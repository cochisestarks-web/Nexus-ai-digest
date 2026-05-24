from fastapi import APIRouter, HTTPException

from models.schemas import DigestItem, GenerateDigestRequest
from services import chroma_service, llm_service

router = APIRouter(prefix="/api", tags=["digest"])


@router.post("/digest", response_model=DigestItem)
async def generate_digest(request: GenerateDigestRequest):
    """
    RAG-powered digest generation.

    Flow:
      1. Retrieve relevant articles from ChromaDB via keyword scoring
      2. Pass retrieved context + profile to Gemini (with Google Search grounding)
      3. Return a structured DigestItem matching the frontend's TypeScript interface
    """
    try:
        context_articles = chroma_service.get_relevant_articles(
            focus_areas=request.profile.focusAreas,
            n_results=10,
        )

        digest = llm_service.generate_digest(
            profile=request.profile,
            previous_titles=request.previousTitles,
            context_articles=context_articles,
        )

        return digest

    except Exception as e:
        print(f"[Digest] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
