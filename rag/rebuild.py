"""Wipe and rebuild the entire RAG index from scratch."""
import yaml
import sqlite3
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rich.console import Console
from ingest import load_config, open_db, ingest_file

console = Console()

def main():
    config = load_config()

    console.print("[bold yellow]Rebuilding RAG index from scratch...[/]")

    client = chromadb.PersistentClient(path=config["stores"]["chroma"])
    try:
        client.delete_collection("memory")
        console.print("  Cleared ChromaDB collection")
    except Exception:
        pass
    collection = client.get_or_create_collection("memory", metadata={"hnsw:space": "cosine"})

    conn = open_db(config["stores"]["metadata"])
    conn.execute("DELETE FROM indexed_files")
    conn.commit()
    console.print("  Cleared metadata DB")

    console.print(f"[dim]Loading model: {config['embedding']['model']}[/]")
    model = SentenceTransformer(config["embedding"]["model"])

    memory_root = Path(config["memory_root"])
    md_files = list(memory_root.rglob("*.md"))
    console.print(f"Indexing {len(md_files)} files...")

    total = 0
    for f in md_files:
        n = ingest_file(f, collection, conn, model)
        console.print(f"  [green]{f.name}[/]: {n} chunks")
        total += n

    console.print(f"\n[bold green]Done.[/] {total} total chunks indexed.")

if __name__ == "__main__":
    main()
