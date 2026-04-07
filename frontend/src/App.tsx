import "./App.css";

import { useState } from "react";
import { useSlideGenerator } from "./hooks/useSlideGenerator";
import { GenerateButton } from "./components/GenerateButton";
import { StatusMessage } from "./components/StatusMessage";
import type { SlideRequest } from "./types/api";
import { useManim } from "./hooks/useManim";
import { ManimPlayer } from "./components/ManimPlayer";

export default function App() {
  const [prompt, setPrompt] = useState<string>("");
  const [slideCount, setSlideCount] = useState<number>(5);
  const { status, loading, generate } = useSlideGenerator();
  const { videoUrl, loading: rloading, error, renderScene } = useManim();

  function handleGenerate() {
    const req: SlideRequest = { prompt, slide_count: slideCount };
    void generate(req);
  }

  return (
    <div
      style={{ maxWidth: 600, margin: "60px auto", fontFamily: "sans-serif" }}
    >
      <h1>AI Slide Generator</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your presentation..."
        rows={4}
        style={{ width: "100%", fontSize: 16 }}
      />
      <div
        style={{
          marginTop: 8,
          marginBottom: 12,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <label style={{ marginRight: 8 }}>Slides:</label>
        <input
          type="number"
          value={slideCount}
          min={1}
          onChange={(e) =>
            setSlideCount(Math.max(1, Number(e.target.value) || 1))
          }
          style={{ width: 64, textAlign: "center", fontSize: 14, padding: 6 }}
        />
      </div>

      <br />
      <GenerateButton onClick={handleGenerate} loading={loading} />
      {status ? <StatusMessage message={status} /> : null}
      <ManimPlayer
        videoUrl={videoUrl}
        loading={rloading}
        error={error}
        onRender={() => void renderScene()}
      />
    </div>
  );
}
