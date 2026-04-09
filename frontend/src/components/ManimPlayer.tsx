interface Props {
  videoUrl: string;
  loading: boolean;
  error: string;
  onRender: () => void;
}

export function ManimPlayer({ videoUrl, loading, error, onRender }: Props) {
  return (
    <div style={{ marginTop: 20 }}>
      <button onClick={onRender} disabled={loading}>
        {loading ? "Rendering..." : "Render Manim Scene"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {videoUrl && (
        <video
          src={videoUrl}
          controls
          style={{ width: "100%", marginTop: 12 }}
        />
      )}
    </div>
  );
}
