#!/usr/bin/env python3
"""Restore the original second-level scholar dashboards and add new papers."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SCHOLARS = ROOT / "2.Scholar"
sys.path.insert(0, str(ROOT / "tools"))
from rebuild_scholar_indexes import rdf_metadata  # noqa: E402

STYLE = """
<style id="current-paper-nav-style">
.current-paper-nav{max-width:1100px;margin:24px auto;padding:0 22px}.current-paper-nav h2{font-size:1.15rem;margin:0 0 14px}.current-paper-nav p{color:#8b8fa3;font-size:.82rem}.current-paper-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}.current-paper-card{display:block;text-decoration:none;color:inherit;background:#1a1d27;border:1px solid #2a2d3a;border-radius:10px;padding:15px 17px;transition:.2s}.current-paper-card:hover{border-color:#60a5fa;transform:translateY(-2px)}.current-paper-card strong{display:block;font-size:.91rem;line-height:1.45}.current-paper-card span{display:block;color:#8b8fa3;font-size:.74rem;margin-top:7px}.current-paper-card.is-new{border-left:4px solid #60a5fa}@media(max-width:650px){.current-paper-grid{grid-template-columns:1fr}}
</style>
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def original_index(name: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:2.Person/{name}/index.html"],
        cwd=ROOT,
        capture_output=True,
    )
    return result.stdout.decode("utf-8") if result.returncode == 0 else None


def repair_paths(content: str, name: str, rdf_name: str | None) -> str:
    content = content.replace("2.Person/", "2.Scholar/")
    content = content.replace(f"{name}/files/", "files/")
    content = content.replace("学习笔记目录.html", "files/index.html")
    content = content.replace('href="files/"', 'href="files/index.html"')
    content = content.replace("href='files/'", "href='files/index.html'")
    content = content.replace("google-scholar.txt", "google_scholar.txt")
    if rdf_name:
        content = content.replace("Exported Items.rdf", rdf_name)
    # The previous generic paper landing page is no longer the third level.
    content = re.sub(r"(files/[^/'\"+]+/)index\.html", r"\1note.html", content)
    return content


def add_current_papers(content: str, scholar: Path) -> str:
    metadata = rdf_metadata(scholar)
    files = scholar / "files"
    folders = sorted((p for p in files.iterdir() if p.is_dir()), key=lambda p: (not p.name.isdigit(), int(p.name) if p.name.isdigit() else p.name)) if files.is_dir() else []
    missing = [folder for folder in folders if not re.search(rf"files/{re.escape(folder.name)}/(?:note|index)\.html", content)]
    content = re.sub(r"<!-- CURRENT-PAPER-NAV START -->.*?<!-- CURRENT-PAPER-NAV END -->", "", content, flags=re.S)
    content = content.replace(STYLE, "")
    if "</head>" in content:
        content = content.replace("</head>", STYLE + "</head>", 1)
    if not missing:
        return content
    cards = []
    for folder in missing:
        data = metadata.get(folder.name, {})
        title = data.get("title") or next((p.stem for p in folder.glob("*.pdf")), f"Paper {folder.name}")
        date = data.get("date") or "Local paper"
        cards.append(f'<a class="current-paper-card is-new" href="files/{quote(folder.name)}/note.html"><strong>{esc(title)}</strong><span>{esc(date)} · Paper {esc(folder.name)} · Open notes →</span></a>')
    block = f'''<!-- CURRENT-PAPER-NAV START -->
<section class="current-paper-nav"><h2>📚 Current Local Papers</h2><p>{len(folders)} papers in the normalized library; cards below supplement entries not present in the original dashboard.</p><div class="current-paper-grid">{"".join(cards)}</div></section>
<!-- CURRENT-PAPER-NAV END -->'''
    marker = "</main>" if "</main>" in content else "</body>"
    return content.replace(marker, block + marker, 1)


def update_counts(content: str, count: int) -> str:
    content = re.sub(r'(<div class="num">)\d+(</div><div class="lbl">Tracked Papers)', rf"\g<1>{count}\2", content, count=1)
    content = re.sub(r'(<div class="stat"><b>)\d+(</b><br>Tracked Papers)', rf"\g<1>{count}\2", content, count=1)
    return content


def main() -> None:
    restored = supplemented = 0
    for scholar in sorted((p for p in SCHOLARS.iterdir() if p.is_dir() and not p.name.startswith(".")), key=lambda p: p.name.casefold()):
        current = (scholar / "index.html").read_text("utf-8") if (scholar / "index.html").is_file() else ""
        original = original_index(scholar.name)
        content = original if original is not None else current
        if original is not None:
            restored += 1
        rdf = next(scholar.glob("*.rdf"), None)
        content = repair_paths(content, scholar.name, rdf.name if rdf else None)
        before = content
        content = add_current_papers(content, scholar)
        if content != before:
            supplemented += 1
        files = scholar / "files"
        count = sum(1 for p in files.iterdir() if p.is_dir()) if files.is_dir() else 0
        content = update_counts(content, count)
        (scholar / "index.html").write_text(content, encoding="utf-8", newline="\n")
    print(f"Restored {restored} original scholar dashboards; supplemented {supplemented} dashboards.")


if __name__ == "__main__":
    main()
