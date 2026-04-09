import { useState } from "react";
import { apiUrl } from "../config/apiBase";

const BACKEND_HINT =
  "Start the API from the backend folder: uvicorn main:app --reload --host 127.0.0.1 --port 8000 (or docker compose up backend).";

function errorTextFromBody(data: unknown, fallback: string): string {
  if (typeof data !== "object" || data === null) return fallback;
  if ("detail" in data) {
    const d = (data as { detail: unknown }).detail;
    if (typeof d === "string") return d;
  }
  if ("message" in data) {
    const m = (data as { message: unknown }).message;
    if (typeof m === "string") return m;
  }
  return fallback;
}

export function useManim() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function renderScene(): Promise<void> {
    setLoading(true);
    setError(null);
    setVideoUrl(null);
    try {
      const res = await fetch(apiUrl("/manim/render"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const raw = await res.text();
      let data: unknown = null;
      try {
        data = raw ? JSON.parse(raw) : null;
      } catch {
        setError(`Error ${res.status}: invalid JSON`);
        return;
      }
      if (!res.ok) {
        setError(errorTextFromBody(data, `Error ${res.status}`));
        return;
      }
      if (
        typeof data === "object" &&
        data !== null &&
        "video_url" in data &&
        typeof (data as { video_url: unknown }).video_url === "string" &&
        (data as { video_url: string }).video_url.length > 0
      ) {
        setVideoUrl((data as { video_url: string }).video_url);
        return;
      }
      setError(null);
    } catch {
      setError(`Cannot reach backend. ${BACKEND_HINT}`);
    } finally {
      setLoading(false);
    }
  }

  return { videoUrl, loading, error, renderScene };
}
