import { useState } from "react";
import type { SlideRequest } from "../types/api";

const GENERATE_URL =
  import.meta.env.VITE_API_BASE_URL != null &&
  String(import.meta.env.VITE_API_BASE_URL).trim() !== ""
    ? `${String(import.meta.env.VITE_API_BASE_URL).replace(/\/$/, "")}/generate`
    : "/api/generate";

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

export function useSlideGenerator() {
  const [status, setStatus] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  async function generate(req: SlideRequest): Promise<void> {
    setLoading(true);
    setStatus("Generating...");
    try {
      const res = await fetch(GENERATE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req),
      });
      const raw = await res.text();
      let data: unknown = null;
      try {
        data = raw ? JSON.parse(raw) : null;
      } catch {
        setStatus(`Error ${res.status}: invalid JSON`);
        return;
      }
      if (!res.ok) {
        setStatus(
          errorTextFromBody(data, `Error ${res.status}`),
        );
        return;
      }
      if (
        typeof data === "object" &&
        data !== null &&
        "message" in data &&
        typeof (data as { message: unknown }).message === "string"
      ) {
        setStatus((data as { message: string }).message);
        return;
      }
      setStatus("Done!");
    } catch {
      setStatus("Cannot reach backend. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  }

  return { status, loading, generate };
}
