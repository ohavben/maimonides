#!/usr/bin/env python3
"""
HCAI build pipeline
  Track A (knowledge/claude/*.md) → Track C (knowledge/reference/*.html)  [MAN-style]
  knowledge/github/**/*.md        → Track B (knowledge/docs/*.pdf)         [chromium]

Usage:
  python3 scripts/build.py              # build all
  python3 scripts/build.py --track c    # Track C only
  python3 scripts/build.py --track b    # Track B only (requires chromium)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRACK_A = ROOT / "knowledge" / "claude"
TRACK_C = ROOT / "knowledge" / "reference"
TRACK_D_GITHUB = ROOT / "knowledge" / "github"
TRACK_B = ROOT / "knowledge" / "docs"

MAN_CSS = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.6;
    background: #0d1117;
    color: #c9d1d9;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 3rem;
  }
  h1 { color: #58a6ff; font-size: 1.4rem; margin-bottom: 0.5rem; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }
  h2 { color: #79c0ff; font-size: 1.1rem; margin: 1.5rem 0 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
  h3 { color: #ffa657; font-size: 1rem; margin: 1rem 0 0.3rem; }
  p { margin-bottom: 0.8rem; }
  code, pre { font-family: inherit; background: #161b22; border: 1px solid #30363d; border-radius: 3px; }
  code { padding: 0.1em 0.3em; color: #f0883e; }
  pre { padding: 1rem; margin: 0.8rem 0; overflow-x: auto; white-space: pre; color: #8b949e; }
  table { border-collapse: collapse; width: 100%; margin: 0.8rem 0; }
  th { background: #161b22; color: #58a6ff; padding: 0.4rem 0.8rem; text-align: left; border: 1px solid #30363d; }
  td { padding: 0.3rem 0.8rem; border: 1px solid #30363d; }
  tr:nth-child(even) td { background: #0d1117; }
  tr:nth-child(odd) td { background: #161b22; }
  ul, ol { margin: 0.5rem 0 0.8rem 1.5rem; }
  li { margin-bottom: 0.2rem; }
  hr { border: none; border-top: 1px solid #30363d; margin: 1.5rem 0; }
  .man-header { display: flex; justify-content: space-between; color: #6e7681; font-size: 0.85rem; margin-bottom: 1.5rem; }
  .man-section { margin: 1.5rem 0; }
  a { color: #58a6ff; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .see-also a { display: block; margin: 0.2rem 0; }
</style>
"""

MAN_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title} — HCAI Reference</title>
  {css}
</head>
<body>
  <div class="man-header">
    <span>HCAI({section})</span>
    <span>Halachic Constitutional AI</span>
    <span>HCAI({section})</span>
  </div>
  {body}
  <div class="man-header" style="margin-top:2rem;">
    <span>Halachic Constitutional AI</span>
    <span>{date}</span>
    <span>HCAI({section})</span>
  </div>
</body>
</html>
"""


def md_to_html_body(md_text: str) -> str:
    """Minimal markdown → HTML for Track C MAN pages."""
    import html as html_lib
    lines = md_text.split("\n")
    out = []
    in_code = False
    in_table = False
    in_ul = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.strip().startswith("```"):
            if not in_code:
                lang = line.strip()[3:].strip()
                out.append(f'<pre><code class="language-{lang}">')
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue

        if in_code:
            out.append(html_lib.escape(line))
            i += 1
            continue

        # Table detection
        if "|" in line and i + 1 < len(lines) and re.match(r"[\s|:-]+$", lines[i + 1]):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<table>")
            headers = [c.strip() for c in line.strip("|").split("|")]
            out.append("<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>")
            i += 2  # skip separator
            while i < len(lines) and "|" in lines[i]:
                cols = [c.strip() for c in lines[i].strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in cols) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        # End table
        if in_table and "|" not in line:
            out.append("</tbody></table>")
            in_table = False

        # Headings
        if line.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h1>{inline_md(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h2>{inline_md(line[3:])}</h2>")
        elif line.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h3>{inline_md(line[4:])}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(line[2:])}</li>")
        elif line.strip() == "---":
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<hr>")
        elif line.strip() == "":
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("")
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<p>{inline_md(line)}</p>")

        i += 1

    if in_ul:
        out.append("</ul>")

    return "\n".join(out)


def inline_md(text: str) -> str:
    """Convert inline markdown (bold, code, links) to HTML."""
    import html as html_lib
    text = html_lib.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def build_track_c():
    """Generate Track C MAN-style HTML from Track A MD files."""
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    TRACK_C.mkdir(parents=True, exist_ok=True)

    source_files = list(TRACK_A.glob("*.md"))
    if not source_files:
        print("  No Track A files found.")
        return

    for src in source_files:
        md = src.read_text(encoding="utf-8")
        title = src.stem.upper()
        section = "1"  # HCAI section 1 = principles/protocols; could be extended

        body = md_to_html_body(md)
        html = MAN_TEMPLATE.format(
            title=title,
            section=section,
            css=MAN_CSS,
            body=body,
            date=today,
        )

        out_path = TRACK_C / (src.stem + ".html")
        out_path.write_text(html, encoding="utf-8")
        print(f"  Track C: {src.name} → {out_path.relative_to(ROOT)}")

    # Build index
    index_links = "\n".join(
        f'<li><a href="{p.stem}.html">{p.stem.upper()}</a> — {_first_line(p)}</li>'
        for p in sorted(source_files)
    )
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>HCAI Reference Index</title>
  {MAN_CSS}
</head>
<body>
  <h1>HCAI Reference Index</h1>
  <p>MAN-style quick reference pages for Halachic Constitutional AI concepts.</p>
  <hr>
  <ul style="list-style:none; margin-left:0;">
    {index_links}
  </ul>
</body>
</html>"""
    (TRACK_C / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Track C: index.html written")


def _first_line(path: Path) -> str:
    """Return first non-empty, non-heading line of a markdown file."""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:80]
    return ""


def build_track_b():
    """Generate Track B PDFs from Track D GitHub MD pages via chromium."""
    TRACK_B.mkdir(parents=True, exist_ok=True)

    chromium = _find_chromium()
    if not chromium:
        print("  chromium not found — skipping Track B PDF generation")
        return

    # For each Track D page, render via chromium
    github_pages = list(TRACK_D_GITHUB.rglob("*.md"))
    if not github_pages:
        print("  No Track D files found — skipping Track B")
        return

    for src in github_pages:
        # Convert MD to HTML first (minimal)
        md = src.read_text(encoding="utf-8")
        tmp_html = TRACK_B / (src.stem + "_tmp.html")
        body = md_to_html_body(md)
        tmp_html.write_text(f"<!DOCTYPE html><html><head>{MAN_CSS}</head><body>{body}</body></html>")

        pdf_path = TRACK_B / (src.stem + ".pdf")
        try:
            subprocess.run([
                chromium,
                "--headless", "--no-sandbox",
                f"--print-to-pdf={pdf_path}",
                "--print-to-pdf-no-header",
                str(tmp_html),
            ], check=True, capture_output=True)
            print(f"  Track B: {src.name} → {pdf_path.relative_to(ROOT)}")
        except subprocess.CalledProcessError as e:
            print(f"  Track B: {src.name} FAILED — {e}")
        finally:
            tmp_html.unlink(missing_ok=True)


def _find_chromium() -> str | None:
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        result = subprocess.run(["which", name], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def main():
    parser = argparse.ArgumentParser(description="HCAI build pipeline")
    parser.add_argument("--track", choices=["a", "b", "c", "all"], default="all",
                        help="Which track to build (default: all)")
    args = parser.parse_args()

    if args.track in ("c", "all"):
        print("Building Track C (MAN-style HTML from Track A)...")
        build_track_c()

    if args.track in ("b", "all"):
        print("Building Track B (PDFs from Track D via chromium)...")
        build_track_b()

    print("Done.")


if __name__ == "__main__":
    main()
