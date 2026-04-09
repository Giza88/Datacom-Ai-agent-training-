/**
 * Dev: leave unset so requests use `/api/...` and Vite proxies to the FastAPI
 * server (see vite.config.ts). Set `VITE_API_BASE_URL` to call the API directly
 * (e.g. `http://127.0.0.1:8000`) when the proxy is not used.
 */
export function apiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL;
  if (typeof raw === "string" && raw.trim() !== "") {
    return raw.replace(/\/$/, "");
  }
  return "";
}

/** FastAPI path only, e.g. `/generate` or `/manim/render` (leading slash). */
export function apiUrl(fastApiPath: string): string {
  const path = fastApiPath.startsWith("/") ? fastApiPath : `/${fastApiPath}`;
  const base = apiBaseUrl();
  if (base) {
    return `${base}${path}`;
  }
  return `/api${path}`;
}
