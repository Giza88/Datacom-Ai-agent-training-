interface Props {
  videoUrl: string | null;
  loading: boolean;
  error: string | null;
  onRender: () => void;
}

export function ManimPlayer({
  videoUrl,
  loading,
  error,
  onRender,
}: Props) {
  return (
    <div style={{ marginTop: 24 }}>
      <button
        type="button"
        onClick={onRender}
        disabled={loading}
        style={{ padding: "10px 16px", fontSize: 15 }}
      >
        {loading ? "Rendering…" : "Render Manim scene"}
      </button>
      {loading && (
        <p style={{ marginTop: 12, color: "#666" }}>Rendering scene…</p>
      )}
      {error && (
        <p style={{ marginTop: 12, color: "#c62828" }}>{error}</p>
      )}
      {videoUrl && (
        <video
          style={{ marginTop: 16, width: "100%", borderRadius: 8 }}
          src={videoUrl}
          controls
          playsInline
        />
      )}
    </div>
  );
}
