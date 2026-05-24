"""
Embedding service using ChromaDB's built-in DefaultEmbeddingFunction.
Uses all-MiniLM-L6-v2 via ONNX runtime — no external API calls needed.
Gemini is still used for generation and Google Search grounding.
"""
from typing import List

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

_ef: DefaultEmbeddingFunction | None = None


def _get_ef() -> DefaultEmbeddingFunction:
    global _ef
    if _ef is None:
        _ef = DefaultEmbeddingFunction()
    return _ef


def embed_text(text: str) -> List[float]:
    ef = _get_ef()
    return list(ef([text])[0])


def embed_texts(texts: List[str]) -> List[List[float]]:
    ef = _get_ef()
    return [list(e) for e in ef(texts)]
