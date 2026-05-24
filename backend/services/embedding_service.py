import os
from typing import List

import google.generativeai as genai_legacy

_configured = False


def _ensure_configured() -> None:
    global _configured
    if not _configured:
        genai_legacy.configure(api_key=os.environ["GEMINI_API_KEY"])
        _configured = True


def embed_text(text: str) -> List[float]:
    _ensure_configured()
    result = genai_legacy.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts sequentially."""
    embeddings = []
    for i, text in enumerate(texts):
        try:
            embeddings.append(embed_text(text))
        except Exception as e:
            print(f"[Embedding] Failed on item {i}: {e}")
            raise
    return embeddings
