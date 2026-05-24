from fastapi import APIRouter, BackgroundTasks

from models.schemas import IngestResponse
from services import chroma_service, rss_service

router = APIRouter(prefix="/api", tags=["ingest"])


def _run_ingestion() -> int:
    articles = rss_service.fetch_all_articles()
    if not articles:
        return 0
    chroma_service.upsert_articles(articles)
    return len(articles)


@router.post("/ingest", response_model=IngestResponse)
async def trigger_ingest(background_tasks: BackgroundTasks):
    """Kick off RSS ingestion in the background."""

    def _bg():
        try:
            count = _run_ingestion()
            print(f"[Ingest] Complete — {count} articles ingested")
        except Exception as e:
            print(f"[Ingest] Failed: {e}")

    background_tasks.add_task(_bg)
    return IngestResponse(
        status="started",
        message="RSS ingestion running in background. Wait a few seconds, then run the pipeline.",
    )


@router.post("/ingest/sync", response_model=IngestResponse)
async def trigger_ingest_sync():
    """Synchronous ingest — waits for completion before responding."""
    try:
        count = _run_ingestion()
        return IngestResponse(
            status="complete",
            message="Ingestion complete.",
            articlesIngested=count,
        )
    except Exception as e:
        return IngestResponse(status="error", message=str(e))


@router.get("/ingest/status")
async def ingest_status():
    count = chroma_service.article_count()
    return {
        "articleCount": count,
        "ready": count > 0,
        "message": f"{count} articles indexed" if count > 0 else "No articles yet — POST /api/ingest to populate",
    }
