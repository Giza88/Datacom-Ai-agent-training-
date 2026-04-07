import { useState } from "react";

const MANIM_RENDER_URL =
  import.meta.env.VITE_API_BASE_URL != null &&
  String(import.meta.env.VITE_API_BASE_URL).trim() !== ""
    ? `${String(import.meta.env.VITE_API_BASE_URL).replace(/\/$/, "")}/manim/render`
    : "/api/manim/render";

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
      const res = await fetch(MANIM_RENDER_URL, {
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
      setError("Cannot reach backend. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  }

  return { videoUrl, loading, error, renderScene };
}
