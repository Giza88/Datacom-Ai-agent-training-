/**
 * Mirrors backend `routes/generate._safe_pptx_filename` for fallback when
 * Content-Disposition is missing (e.g. stripped by a proxy).
 */
export function safePptxFilenameFromPrompt(prompt: string, maxStem = 30): string {
  let stem = (prompt ?? "").trim().slice(0, maxStem);
  stem = stem.replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_");
  stem = stem.replace(/^[ .]+|[ .]+$/g, "") || "slides";
  return `${stem}.pptx`;
}

/**
 * Parse filename from Content-Disposition (RFC 5987 filename* and filename="...").
 */
export function parseFilenameFromContentDisposition(
  header: string | null,
): string | null {
  if (!header) return null;

  const star = /filename\*=UTF-8''([^;\s]+)/i.exec(header);
  if (star?.[1]) {
    try {
      return decodeURIComponent(star[1].replace(/["']/g, ""));
    } catch {
      return null;
    }
  }

  const quoted = /filename="((?:\\.|[^"\\])*)"/i.exec(header);
  if (quoted?.[1]) {
    return quoted[1].replace(/\\(.)/g, "$1");
  }

  const plain = /filename=([^;\s]+)/i.exec(header);
  if (plain?.[1]) {
    return plain[1].replace(/^["']|["']$/g, "");
  }

  return null;
}
