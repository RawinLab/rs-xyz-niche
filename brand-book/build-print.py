#!/usr/bin/env python3
"""Build a single print.html bundling cover + all 20 sections for PDF generation."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SECTIONS_DIR = ROOT / "sections"
INDEX = ROOT / "index.html"
OUT = ROOT / "print.html"

MAIN_RE = re.compile(r"<main[^>]*>(.*?)</main>", re.DOTALL | re.IGNORECASE)
SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
HEAD_STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)

def extract_main(html: str, source: str) -> str:
    m = MAIN_RE.search(html)
    if not m:
        raise SystemExit(f"no <main> found in {source}")
    return m.group(1).strip()

def extract_inline_styles(html: str) -> str:
    head_match = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    if not head_match:
        return ""
    head = head_match.group(1)
    return "\n".join(m.group(1) for m in HEAD_STYLE_RE.finditer(head))

def main():
    section_files = sorted(SECTIONS_DIR.glob("*.html"))
    print(f"found {len(section_files)} sections")

    # Cover from index.html — extract <main> only
    index_html = INDEX.read_text(encoding="utf-8")
    cover_main = extract_main(index_html, "index.html")

    # Each section's <main> + their inline <style> blocks
    parts = [cover_main]
    inline_styles = []
    for sf in section_files:
        html = sf.read_text(encoding="utf-8")
        parts.append(f'<div class="page-break"></div>')
        section_main = extract_main(html, sf.name)
        # Sections live in brand-book/sections/ and reference ../assets/
        # print.html lives in brand-book/ — so rewrite ../assets → assets
        section_main = section_main.replace('src="../assets/', 'src="assets/')
        section_main = section_main.replace("src='../assets/", "src='assets/")
        section_main = section_main.replace('href="../assets/', 'href="assets/')
        parts.append(section_main)
        inline_styles.append(f"/* {sf.name} */\n" + extract_inline_styles(html))

    combined_inline = "\n".join(inline_styles)

    print_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NICHE Brand Book — Print Edition</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;1,400&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400;1,9..144,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/book.css">
<style>
{combined_inline}

/* ====== PRINT-SPECIFIC ====== */
@page {{
  size: A4;
  margin: 18mm 16mm;
}}

html, body {{
  background: var(--color-surface-base);
}}

.topbar, .sidebar, nav.topbar, .progress-bar, .nav-toggle {{
  display: none !important;
}}

.book-content {{
  margin-left: 0 !important;
  padding: 0 !important;
  max-width: 100% !important;
}}

.page-break {{
  page-break-before: always;
  break-before: page;
  height: 0;
}}

/* Avoid breaks inside critical blocks */
.swatch, .type-row, .contrast-row, figure, .demo-card, .logo-display {{
  page-break-inside: avoid;
  break-inside: avoid;
}}

/* Suppress motion in print */
*, *::before, *::after {{
  animation: none !important;
  transition: none !important;
}}

/* CRITICAL: force all reveal-on-scroll content visible in print
   (IntersectionObserver doesn't fire for offscreen elements without a scroll) */
.reveal-on-scroll,
.reveal,
[data-reveal],
.fade-in,
.scroll-reveal {{
  opacity: 1 !important;
  transform: none !important;
  visibility: visible !important;
}}

/* Force any opacity:0 utility classes visible in print */
.opacity-0, .invisible {{
  opacity: 1 !important;
  visibility: visible !important;
}}

/* Make hero sections fit on print pages */
.section-hero, .cover-hero {{
  min-height: auto !important;
  padding: 24mm 0 16mm !important;
}}

/* Image sizing */
img {{
  max-width: 100% !important;
  height: auto !important;
  page-break-inside: avoid;
}}

/* Hide interactive elements that don't make sense in print */
button, .clickable-hex {{
  pointer-events: none;
}}

/* TOC link colors visible in print */
a {{
  color: var(--color-surface-ink);
  text-decoration: none;
}}

/* Show URL after links in print? — disabled to keep clean */
</style>
</head>
<body>
{"".join(parts)}
</body>
</html>
"""
    OUT.write_text(print_html, encoding="utf-8")
    print(f"wrote {OUT} ({len(print_html):,} bytes)")

if __name__ == "__main__":
    main()
