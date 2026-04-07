interface Props {
  onClick: () => void;
  loading: boolean;
  disabled?: boolean;
}

export function GenerateButton({ onClick, loading, disabled }: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled ?? loading}
      style={{ marginTop: 12, padding: "10px 24px", fontSize: 16 }}
    >
      {loading ? "Generating..." : "Generate Slides"}
    </button>
  );
}
