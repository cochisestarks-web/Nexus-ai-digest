from pydantic import BaseModel
from typing import List


class GroundingSource(BaseModel):
    title: str
    uri: str


class DigestItem(BaseModel):
    id: str
    timestamp: int
    title: str
    summary: str
    keyTakeaways: List[str]
    technicalAnalysis: str
    sources: List[GroundingSource]
    impactScore: int


class TechnicalProfile(BaseModel):
    depth: str  # 'Hobbyist' | 'Software Engineer' | 'ML Researcher' | 'Strategic Executive'
    focusAreas: List[str]
    digestInterval: str  # '4h' | '12h' | '24h'
    notificationEnabled: bool


class GenerateDigestRequest(BaseModel):
    profile: TechnicalProfile
    previousTitles: List[str] = []


class IngestResponse(BaseModel):
    status: str
    message: str
    articlesIngested: int = 0
