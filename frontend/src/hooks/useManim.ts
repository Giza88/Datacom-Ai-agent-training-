import { useState } from "react";
import { apiUrl } from "../config/apiBase";

export function useManim() {
  const [videoUrl, setVideoUrl] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  async function renderScene(sceneClass: string = "TitleSlide") {
    setLoading(true);
    setError("");
    setVideoUrl("");

    try {
      const renderUrl = `${apiUrl("/render")}?${new URLSearchParams({
        scene_class: sceneClass,
      })}`;
      const res = await fetch(renderUrl, {
        method: "POST",
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
