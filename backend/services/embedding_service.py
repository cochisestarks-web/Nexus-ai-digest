"""
Embedding service using google-generativeai legacy SDK with embedding-001.
embedding-001 is stable on the v1beta endpoint that AI Studio keys support.
768-dimensional embeddings, no local model — pure API call.
"""
import os
from typing import List

import google.generativeai as genai_legacy

_configured = False


def _ensure_configured() -> None:
    global _configured
    if not _configured:
        genai_legacy.configure(api_key=os.environ["GEMINI_API_KEY"])
        _configured = True


def embed_text(text: str, task_type: str = "retrieval_document") -> List[float]:
    _ensure_configured()
    result = genai_legacy.embed_content(
        model="models/embedding-001",
        content=text,
        task_type=task_type,
    )
    return result["embedding"]


def embed_query(text: str) -> List[float]:
    """Embed a search query (uses retrieval_query task type for better recall)."""
    return embed_text(text, task_type="retrieval_query")


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of documents sequentially."""
    embeddings = []
    for i, text in enumerate(texts):
        try:
            embeddings.append(embed_text(text))
        except Exception as e:
            print(f"[Embedding] Failed on item {i}: {e}")
            raise
    return embeddings
