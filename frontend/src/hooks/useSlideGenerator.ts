import { useState } from "react";
import type { SlideRequest } from "../types/api";
import {
  parseFilenameFromContentDisposition,
  safePptxFilenameFromPrompt,
} from "../utils/pptxDownloadFilename";

export function useSlideGenerator() {
  const [status, setStatus] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  async function generate(req: SlideRequest): Promise<void> {
    setLoading(true);
    setStatus("Generating AI slides...");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req),
      });
      if (!res.ok) {
        const t = await res.text();
        setStatus(`Error ${res.status}: ${t || "unknown"}`);
        return;
      }
      const contentDisposition = res.headers.get("Content-Disposition");
      const blob: Blob = await res.blob();
      const downloadName =
        parseFilenameFromContentDisposition(contentDisposition) ??
        safePptxFilenameFromPrompt(req.prompt);
      const a = document.createElement("a") as HTMLAnchorElement;
      a.href = URL.createObjectURL(blob);
      a.download = downloadName;
      a.click();
      URL.revokeObjectURL(a.href);
      setStatus("✅ AI slides downloaded!");
    } catch {
      setStatus("Cannot reach backend.");
    } finally {
      setLoading(false);
    }
  }

  return { status, loading, generate };
}
