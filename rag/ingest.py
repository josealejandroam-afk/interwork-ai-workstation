"""Ingest markdown memory files into ChromaDB + metadata SQLite."""
import sys
import sqlite3
import hashlib
import re
import yaml
import frontmatter
import chromadb
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.progress import track

console = Console()

def load_config():
    return yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())

def open_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS indexed_files (
            path TEXT PRIMARY KEY,
            sha256 TEXT,
            mtime REAL,
            size INTEGER,
            last_indexed TEXT,
            chunk_count INTEGER
        )
    """)
    conn.commit()
    return conn

def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def needs_reindex(conn, path):
    row = conn.execute(
        "SELECT sha256, mtime, size FROM indexed_files WHERE path = ?", (str(path),)
    ).fetchone()
    if row is None:
        return True
    sha, mtime, size = row
    stat = Path(path).stat()
    if abs(stat.st_mtime - mtime) > 1 or stat.st_size != size:
        return file_hash(path) != sha
    return False

def chunk_text(text, target=4000, overlap=600):
    sections = re.split(r'\n(?=#{1,3} )', text)
    chunks, current = [], ""
    for section in sections:
        if len(current) + len(section) < target:
            current += ("\n" if current else "") + section
        else:
            if current:
                chunks.append(current)
                current = current[-overlap:] + "\n" + section
            else:
                # Section larger than target — split by paragraphs
                for para in section.split("\n\n"):
                    if len(current) + len(para) < target:
                        current += ("\n\n" if current else "") + para
                    else:
                        if current:
                            chunks.append(current)
                            current = current[-overlap:] + "\n\n" + para
                        else:
                            chunks.append(para)
                            current = ""
    if current.strip():
        chunks.append(current)
    return chunks or [text]

def extract_meta(post_meta):
    """Flatten nested metadata.type/status/confidence or top-level."""
    nested = post_meta.get("metadata", {}) or {}
    def get(key):
        return str(nested.get(key, post_meta.get(key, "")))
    return get("type"), get("status"), get("confidence"), get("updated"), get("source")

def ingest_file(path, collection, conn, model):
    path = Path(path)
    try:
        post = frontmatter.load(str(path))
        body, meta = post.content, dict(post.metadata)
    except Exception:
        body = path.read_text(encoding="utf-8", errors="ignore")
        meta = {}

    doc_type, status, confidence, updated, source = extract_meta(meta)

    # Summary chunk: file name + frontmatter + first 20 lines
    lines = body.split("\n")
    summary = f"File: {path.name}\nFolder: {path.parent.name}\n"
    if meta:
        summary += yaml.dump(meta, allow_unicode=True, default_flow_style=False)
    summary += "\n" + "\n".join(lines[:20])

    body_chunks = chunk_text(body)
    all_chunks = [summary] + body_chunks

    # Remove old entries for this file
    old = collection.get(where={"source_path": str(path)})["ids"]
    if old:
        collection.delete(ids=old)

    embeddings = model.encode(all_chunks, show_progress_bar=False).tolist()
    ids = [f"{path}::chunk{i}" for i in range(len(all_chunks))]
    metadatas = [{
        "source_path": str(path),
        "file_name": path.name,
        "folder": path.parent.name,
        "type": doc_type,
        "status": status,
        "confidence": confidence,
        "updated": updated,
        "chunk_index": i,
        "is_summary": str(i == 0),
    } for i in range(len(all_chunks))]

    collection.add(documents=all_chunks, embeddings=embeddings, metadatas=metadatas, ids=ids)

    stat = path.stat()
    conn.execute(
        "INSERT OR REPLACE INTO indexed_files VALUES (?,?,?,?,?,?)",
        (str(path), file_hash(path), stat.st_mtime, stat.st_size,
         datetime.now().isoformat(), len(all_chunks))
    )
    conn.commit()
    return len(all_chunks)

def main(force=False):
    config = load_config()
    memory_root = Path(config["memory_root"])

    console.print(f"[bold cyan]Loading embedding model:[/] {config['embedding']['model']}")
    model = SentenceTransformer(config["embedding"]["model"])

    client = chromadb.PersistentClient(path=config["stores"]["chroma"])
    collection = client.get_or_create_collection("memory", metadata={"hnsw:space": "cosine"})
    conn = open_db(config["stores"]["metadata"])

    md_files = list(memory_root.rglob("*.md"))
    console.print(f"[bold]Found {len(md_files)} markdown files[/]")

    total_chunks, skipped = 0, 0
    for f in track(md_files, description="Indexing..."):
        if force or needs_reindex(conn, f):
            n = ingest_file(f, collection, conn, model)
            total_chunks += n
        else:
            skipped += 1

    console.print(f"\n[green]Done.[/] {total_chunks} new chunks indexed, {skipped} skipped. "
                  f"Total in store: [bold]{collection.count()}[/]")

if __name__ == "__main__":
    main(force="--force" in sys.argv)
