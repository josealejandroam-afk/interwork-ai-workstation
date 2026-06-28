"""Watch memory folder and auto-reindex on changes."""
import time
import yaml
import chromadb
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sentence_transformers import SentenceTransformer
from rich.console import Console
from ingest import load_config, open_db, ingest_file

console = Console()

def get_log_path(config):
    log_dir = Path(config["rag_root"]) / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir / "watch.log"

def log_event(log_path, event_type, file_path, chunks=None, error=None):
    ts = datetime.now().isoformat(timespec="seconds")
    if error:
        line = f"{ts} ERROR {event_type} {file_path} — {error}\n"
    elif chunks is not None:
        line = f"{ts} OK    {event_type} {file_path} — {chunks} chunks\n"
    else:
        line = f"{ts} OK    {event_type} {file_path}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line)
    console.print(f"[dim]{line.strip()}[/]")

class MemoryWatcher(FileSystemEventHandler):
    def __init__(self, collection, conn, model, log_path):
        self.collection = collection
        self.conn = conn
        self.model = model
        self.log_path = log_path

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            console.print(f"[yellow]Modified:[/] {event.src_path}")
            try:
                n = ingest_file(event.src_path, self.collection, self.conn, self.model)
                log_event(self.log_path, "MODIFIED", event.src_path, chunks=n)
            except Exception as e:
                log_event(self.log_path, "MODIFIED", event.src_path, error=str(e))

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            console.print(f"[green]Created:[/] {event.src_path}")
            try:
                n = ingest_file(event.src_path, self.collection, self.conn, self.model)
                log_event(self.log_path, "CREATED", event.src_path, chunks=n)
            except Exception as e:
                log_event(self.log_path, "CREATED", event.src_path, error=str(e))

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            console.print(f"[red]Deleted:[/] {event.src_path}")
            try:
                ids = self.collection.get(where={"source_path": event.src_path})["ids"]
                if ids:
                    self.collection.delete(ids=ids)
                self.conn.execute("DELETE FROM indexed_files WHERE path = ?", (event.src_path,))
                self.conn.commit()
                log_event(self.log_path, "DELETED", event.src_path)
            except Exception as e:
                log_event(self.log_path, "DELETED", event.src_path, error=str(e))

def main():
    config = load_config()
    memory_root = Path(config["memory_root"])
    log_path = get_log_path(config)

    console.print(f"[dim]Loading model: {config['embedding']['model']}[/]")
    model = SentenceTransformer(config["embedding"]["model"])
    client = chromadb.PersistentClient(path=config["stores"]["chroma"])
    collection = client.get_or_create_collection("memory", metadata={"hnsw:space": "cosine"})
    conn = open_db(config["stores"]["metadata"])

    log_event(log_path, "STARTUP", str(memory_root))

    handler = MemoryWatcher(collection, conn, model, log_path)
    observer = Observer()
    observer.schedule(handler, str(memory_root), recursive=True)
    observer.start()

    console.print(f"[bold cyan]Watching[/] {memory_root} for changes... (Ctrl+C to stop)")
    console.print(f"[dim]Logging to {log_path}[/]")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_event(log_path, "SHUTDOWN", str(memory_root))
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
