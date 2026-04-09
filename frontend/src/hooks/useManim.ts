import { useState } from "react";

export function useManim() {
  const [videoUrl, setVideoUrl] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  async function renderScene(sceneClass: string = "TitleSlide") {
    setLoading(true);
    setError("");
    setVideoUrl("");

    try {
      const res = await fetch("/api/render?scene_class=" + sceneClass, {
        method: "POST"
      });

      if (!res.ok) {
        const t = await res.text();
        setError("Render failed: " + t);
        return;
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);
    } catch {
      setError("Cannot reach backend.");
    } finally {
      setLoading(false);
    }
  }

  return { videoUrl, loading, error, renderScene };
}
