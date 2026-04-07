interface Props {
  message: string;
}

export function StatusMessage({ message }: Props) {
  return <p className="status-message">{message}</p>;
}
