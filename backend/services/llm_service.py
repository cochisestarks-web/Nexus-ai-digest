import json
import os
import re
import time
import uuid
from typing import List, Dict

from google import genai
from google.genai import types

from models.schemas import DigestItem, GroundingSource, TechnicalProfile

DEFAULT_MODEL = "gemini-2.5-flash"

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def _extract_json(text: str) -> dict:
    """Robustly extract a JSON object from model output that may contain markdown."""
    # 1. Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Strip markdown code fences
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        try:
            return json.loads(fence_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. Find the outermost JSON object
    obj_match = re.search(r"\{[\s\S]*\}", text)
    if obj_match:
        try:
            return json.loads(obj_match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from model output. Raw (first 300 chars): {text[:300]}")


def _build_prompt(
    profile: TechnicalProfile,
    previous_titles: List[str],
    context_articles: List[Dict],
) -> str:
    context_block = ""
    if context_articles:
        context_block = "\n## Retrieved Context (from RSS-ingested AI news):\n"
        for i, article in enumerate(context_articles, 1):
            snippet = article["text"][:600].replace("\n", " ")
            context_block += f"\n{i}. [{article['source']}] **{article['title']}**\n   {snippet}\n"

    dedup_clause = (
        f"Do NOT cover topics already reported in these previous digest titles: {', '.join(previous_titles)}."
        if previous_titles
        else "No deduplication constraints."
    )

    return f"""You are a senior AI Intelligence Analyst. Generate a structured knowledge digest.

## User Profile
- Technical Depth: {profile.depth}
- Focus Areas: {', '.join(profile.focusAreas)}
{context_block}
## Instructions
1. Use Google Search to find the latest AI developments from the last 24 hours.
2. Prioritize topics matching the user's focus areas: {', '.join(profile.focusAreas)}.
3. {dedup_clause}
4. Calibrate all explanations for a {profile.depth}.
5. If RSS context was provided above, incorporate relevant articles to enrich the digest.

## Required Output Format
Return ONLY a valid JSON object — no markdown, no code fences, no extra text:
{{
  "title": "Concise headline for today's top AI development (max 80 chars)",
  "summary": "2-3 sentence executive summary of the most impactful developments",
  "keyTakeaways": [
    "Specific, actionable takeaway 1",
    "Specific, actionable takeaway 2",
    "Specific, actionable takeaway 3",
    "Specific, actionable takeaway 4",
    "Specific, actionable takeaway 5"
  ],
  "technicalAnalysis": "2-3 paragraph deep-dive into the how and why. Explain architectures, mechanisms, or strategic implications appropriate for a {profile.depth}.",
  "impactScore": 7
}}"""


def generate_digest(
    profile: TechnicalProfile,
    previous_titles: List[str],
    context_articles: List[Dict],
) -> DigestItem:
    client = _get_client()
    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)

    prompt = _build_prompt(profile, previous_titles, context_articles)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.7,
        ),
    )

    raw_text = response.text or ""

    # Extract grounding sources from search metadata
    sources: List[GroundingSource] = []
    try:
        candidate = response.candidates[0] if response.candidates else None
        if candidate and candidate.grounding_metadata:
            for chunk in candidate.grounding_metadata.grounding_chunks or []:
                if hasattr(chunk, "web") and chunk.web and chunk.web.uri:
                    sources.append(
                        GroundingSource(
                            title=chunk.web.title or "Source",
                            uri=chunk.web.uri,
                        )
                    )
    except Exception as e:
        print(f"[LLM] Could not extract grounding sources: {e}")

    # Parse the JSON payload
    data = _extract_json(raw_text)

    return DigestItem(
        id=str(uuid.uuid4()),
        timestamp=int(time.time() * 1000),
        title=data.get("title", "Daily AI Intelligence Report"),
        summary=data.get("summary", ""),
        keyTakeaways=data.get("keyTakeaways", []),
        technicalAnalysis=data.get("technicalAnalysis", ""),
        sources=sources,
        impactScore=max(1, min(10, int(data.get("impactScore", 7)))),
    )
