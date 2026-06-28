"""RAG status report — shows indexed files, last ingest, chunk count, DB size, recent errors."""
import sqlite3
import yaml
import chromadb
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from ingest import load_config

console = Console()

def main():
    config = load_config()
    rag_root = Path(config["rag_root"])
    chroma_path = config["stores"]["chroma"]
    meta_path = config["stores"]["metadata"]
    log_path = rag_root / "logs" / "watch.log"

    console.print("\n[bold cyan]RAG Status[/]\n")

    # Chroma chunk count
    try:
        client = chromadb.PersistentClient(path=chroma_path)
        collection = client.get_or_create_collection("memory", metadata={"hnsw:space": "cosine"})
        chunk_count = collection.count()
    except Exception as e:
        chunk_count = f"ERROR: {e}"

    # DB size
    chroma_dir = Path(chroma_path)
    db_size_mb = sum(f.stat().st_size for f in chroma_dir.rglob("*") if f.is_file()) / 1e6 if chroma_dir.exists() else 0

    # Indexed files from SQLite
    indexed_files = []
    last_ingest = None
    try:
        conn = sqlite3.connect(meta_path)
        rows = conn.execute("SELECT path, last_indexed, chunk_count FROM indexed_files ORDER BY last_indexed DESC").fetchall()
        for path, last_idx, chunks in rows:
            indexed_files.append((Path(path).name, last_idx, chunks))
        if rows:
            last_ingest = rows[0][1]
        conn.close()
    except Exception as e:
        indexed_files = [("ERROR", str(e), 0)]

    # Recent log entries (last 10 lines)
    recent_log = []
    errors = []
    if log_path.exists():
        lines = log_path.read_text(encoding="utf-8").splitlines()
        recent_log = lines[-10:]
        errors = [l for l in lines if "ERROR" in l][-5:]

    # Print summary
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold", no_wrap=True)
    table.add_column()
    table.add_row("Embedding model", config["embedding"]["model"])
    table.add_row("Memory root", config["memory_root"])
    table.add_row("Chroma DB path", chroma_path)
    table.add_row("Chunk count", str(chunk_count))
    table.add_row("DB size", f"{db_size_mb:.1f} MB")
    table.add_row("Indexed files", str(len(indexed_files)))
    table.add_row("Last ingest", last_ingest or "never")
    console.print(table)

    if indexed_files:
        console.print("\n[bold]Indexed Files:[/]")
        t2 = Table("File", "Last Indexed", "Chunks", show_header=True)
        for name, ts, chunks in indexed_files:
            t2.add_row(name, ts[:19] if ts else "", str(chunks))
        console.print(t2)

    if errors:
        console.print(f"\n[bold red]Recent Errors ({len(errors)}):[/]")
        for e in errors:
            console.print(f"  [red]{e}[/]")
    else:
        console.print("\n[green]No errors in log.[/]")

    if recent_log:
        console.print("\n[bold]Recent Log (last 10):[/]")
        for line in recent_log:
            color = "red" if "ERROR" in line else "dim"
            console.print(f"  [{color}]{line}[/{color}]")

if __name__ == "__main__":
    main()
