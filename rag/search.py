"""Hybrid search: BM25 + vector + recency boost, returns cited results."""
import sys
import yaml
import bm25s
import numpy as np
import chromadb
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def load_config():
    return yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())

def recency_boost(updated_str):
    if not updated_str:
        return 0.0
    try:
        d = datetime.fromisoformat(str(updated_str))
        return max(0.0, 1.0 - (datetime.now() - d).days / 365)
    except Exception:
        return 0.0

def status_boost(status):
    return {"active": 0.8, "uncertain": 0.4, "archived": 0.0}.get(str(status).lower(), 0.3)

def search(query, top_k=None, verbose=True):
    config = load_config()
    w = config["retrieval"]["weights"]
    top_k = top_k or config["retrieval"]["final_top_k"]

    if verbose:
        console.print(f"[dim]Loading model...[/]")
    model = SentenceTransformer(config["embedding"]["model"])

    client = chromadb.PersistentClient(path=config["stores"]["chroma"])
    collection = client.get_or_create_collection("memory", metadata={"hnsw:space": "cosine"})

    total = collection.count()
    if total == 0:
        console.print("[red]Index is empty — run: uv run python ingest.py[/]")
        return []

    # --- Vector search ---
    q_emb = model.encode([query]).tolist()
    vk = min(config["retrieval"]["vector_top_k"], total)
    vres = collection.query(query_embeddings=q_emb, n_results=vk,
                            include=["documents", "metadatas", "distances"])

    # --- BM25 search (build from full corpus) ---
    all_docs = collection.get(include=["documents", "metadatas"])
    corpus_texts = all_docs["documents"]
    corpus_ids = all_docs["ids"]

    corpus_tokens = bm25s.tokenize(corpus_texts, stopwords="en", show_progress=False)
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    bk = min(config["retrieval"]["bm25_top_k"], total)
    q_tokens = bm25s.tokenize([query], stopwords="en", show_progress=False)
    b_results, b_scores = retriever.retrieve(q_tokens, k=bk)

    # --- Merge scores ---
    scores = {}

    for doc_id, dist, meta, doc in zip(
        vres["ids"][0], vres["distances"][0],
        vres["metadatas"][0], vres["documents"][0]
    ):
        scores[doc_id] = {"vector": max(0.0, 1.0 - dist), "bm25": 0.0, "meta": meta, "doc": doc}

    max_bm25 = float(b_scores[0].max()) if b_scores[0].max() > 0 else 1.0
    for idx, score in zip(b_results[0], b_scores[0]):
        did = corpus_ids[idx]
        norm = float(score) / max_bm25
        if did in scores:
            scores[did]["bm25"] = norm
        else:
            scores[did] = {"vector": 0.0, "bm25": norm,
                           "meta": all_docs["metadatas"][idx],
                           "doc": corpus_texts[idx]}

    results = []
    for did, s in scores.items():
        m = s["meta"]
        rec = recency_boost(m.get("updated", "")) * 0.7 + status_boost(m.get("status", "")) * 0.3
        final = w["vector"] * s["vector"] + w["bm25"] * s["bm25"] + w["recency"] * rec
        results.append({
            "id": did,
            "score": final,
            "source": m.get("source_path", ""),
            "file": m.get("file_name", ""),
            "folder": m.get("folder", ""),
            "type": m.get("type", ""),
            "status": m.get("status", ""),
            "chunk": s["doc"],
            "chunk_index": m.get("chunk_index", 0),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def format_citation(r):
    return f"[source: {r['source']}]"

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Query: ")
    results = search(query)

    console.print(f"\n[bold cyan]Results for:[/] {query}\n")
    for i, r in enumerate(results, 1):
        header = f"[{i}] {r['file']}  score={r['score']:.3f}  type={r['type']}  status={r['status']}"
        citation = format_citation(r)
        snippet = r["chunk"][:400].strip().replace("\n", " ").encode("ascii", errors="replace").decode("ascii")
        console.print(Panel(
            f"[dim]{citation}[/]\n\n{snippet}...",
            title=header, expand=False
        ))
