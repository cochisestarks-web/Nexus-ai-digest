from fastapi import APIRouter, HTTPException

from models.schemas import DigestItem, GenerateDigestRequest
from services import chroma_service, embedding_service, llm_service

router = APIRouter(prefix="/api", tags=["digest"])


@router.post("/digest", response_model=DigestItem)
async def generate_digest(request: GenerateDigestRequest):
    """
    RAG-powered digest generation.

    Flow:
      1. Embed the user's profile (depth + focus areas) as a semantic query
      2. Retrieve the top-K relevant articles from ChromaDB
      3. Pass retrieved context + profile to Gemini (with Google Search grounding)
      4. Return a structured DigestItem matching the frontend's TypeScript interface
    """
    try:
        # Step 1: Embed profile as a query
        query = f"{request.profile.depth}: {', '.join(request.profile.focusAreas)}"
        query_embedding = embedding_service.embed_text(query)

        # Step 2: Retrieve context from vector store
        context_articles = chroma_service.query_articles(query_embedding, n_results=10)

        # Step 3: Generate with LLM
        digest = llm_service.generate_digest(
            profile=request.profile,
            previous_titles=request.previousTitles,
            context_articles=context_articles,
        )

        return digest

    except Exception as e:
        print(f"[Digest] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
