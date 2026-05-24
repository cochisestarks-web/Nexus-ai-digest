"""
ChromaDB document store with keyword-based retrieval.

Articles are stored with dummy single-dimension embeddings so ChromaDB
never loads a local ML model. Retrieval uses keyword scoring against
the user's focus areas — lightweight, zero API calls.
"""
import os
from typing import List, Dict

import chromadb

COLLECTION_NAME = "ai_articles"

_chroma_client: chromadb.PersistentClient | None = None
_collection: chromadb.Collection | None = None


def _get_collection() -> chromadb.Collection:
    global _chroma_client, _collection
    if _collection is None:
        db_path = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
        _chroma_client = chromadb.PersistentClient(path=db_path)
        # Dimension=1 dummy embeddings — no embedding model ever loaded
        _collection = _chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def upsert_articles(articles: List[Dict]) -> None:
    collection = _get_collection()
    # Provide a dummy 1-dim embedding per article so ChromaDB never invokes
    # its default embedding function (which would OOM on the free tier).
    dummy_embeddings = [[0.0]] * len(articles)
    collection.upsert(
        ids=[a["id"] for a in articles],
        embeddings=dummy_embeddings,
        documents=[a["text"] for a in articles],
        metadatas=[
            {
                "title": a["title"],
                "url": a["url"],
                "source": a["source"],
                "published": a.get("published", ""),
            }
            for a in articles
        ],
    )
    print(f"[Chroma] Upserted {len(articles)} articles into '{COLLECTION_NAME}'")


def get_relevant_articles(focus_areas: List[str], n_results: int = 10) -> List[Dict]:
    """
    Retrieve articles most relevant to the user's focus areas using keyword scoring.
    Each focus area term found in the article text adds 1 to that article's score.
    """
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        print("[Chroma] Collection is empty — run /api/ingest first")
        return []

    all_results = collection.get(include=["documents", "metadatas"])
    docs = all_results.get("documents") or []
    metas = all_results.get("metadatas") or []

    scored: List[Dict] = []
    for doc, meta in zip(docs, metas):
        doc_lower = doc.lower()
        score = sum(1 for area in focus_areas if area.lower() in doc_lower)
        scored.append(
            {
                "_score": score,
                "text": doc,
                "title": meta.get("title", ""),
                "url": meta.get("url", ""),
                "source": meta.get("source", ""),
            }
        )

    scored.sort(key=lambda x: x["_score"], reverse=True)

    return [
        {"text": a["text"], "title": a["title"], "url": a["url"], "source": a["source"]}
        for a in scored[:n_results]
    ]


def article_count() -> int:
    return _get_collection().count()
