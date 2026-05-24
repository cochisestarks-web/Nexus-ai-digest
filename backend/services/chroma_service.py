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
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def upsert_articles(articles: List[Dict], embeddings: List[List[float]]) -> None:
    collection = _get_collection()
    collection.upsert(
        ids=[a["id"] for a in articles],
        embeddings=embeddings,
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


def query_articles(query_embedding: List[float], n_results: int = 10) -> List[Dict]:
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        print("[Chroma] Collection is empty — run /api/ingest first")
        return []

    n_results = min(n_results, count)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"],
    )

    articles = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    for doc, meta in zip(docs, metas):
        articles.append(
            {
                "text": doc,
                "title": meta.get("title", ""),
                "url": meta.get("url", ""),
                "source": meta.get("source", ""),
            }
        )

    return articles


def article_count() -> int:
    return _get_collection().count()
