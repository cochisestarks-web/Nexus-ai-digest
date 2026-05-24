import { TechnicalProfile, DigestItem } from "../types";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class GeminiService {
  async generateDigest(
    profile: TechnicalProfile,
    previousTitles: string[] = []
  ): Promise<DigestItem> {
    const response = await fetch(`${API_BASE}/api/digest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, previousTitles }),
    });

    if (!response.ok) {
      let detail = `HTTP ${response.status}`;
      try {
        const err = await response.json();
        detail = err.detail || detail;
      } catch {}
      throw new Error(detail);
    }

    return response.json() as Promise<DigestItem>;
  }
}
