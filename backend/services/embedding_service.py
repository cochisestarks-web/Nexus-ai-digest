import os
from typing import List

from google import genai

EMBEDDING_MODEL = "text-embedding-004"

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def embed_text(text: str) -> List[float]:
    client = _get_client()
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return list(result.embeddings[0].values)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts sequentially. Rate-limited by Gemini API."""
    embeddings = []
    for i, text in enumerate(texts):
        try:
            embeddings.append(embed_text(text))
        except Exception as e:
            print(f"[Embedding] Failed on item {i}: {e}")
            raise
    return embeddings
