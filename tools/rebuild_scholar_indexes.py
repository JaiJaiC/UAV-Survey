#!/usr/bin/env python3
"""Normalize 2.Scholar and rebuild its directory indexes.

Canonical layout:

    2.Scholar/<Scholar>/index.html
    2.Scholar/<Scholar>/files/<paper>/index.html
    2.Scholar/<Scholar>/files/<paper>/note.html
"""

from __future__ import annotations

import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SCHOLARS = ROOT / "2.Scholar"

DESCRIPTIONS = {
    "Tairan He": "CMU · Legged Robots · Locomotion",
    "Chao Yan": "NUDT · Multi-UAV · Swarm",
    "Dario Floreano": "EPFL · Bio-inspired Robotics · Small Drones",
    "Davide Scaramuzza": "UZH · Agile Flight · Event Cameras",
    "Fei Gao": "ZJU · Trajectory Planning · Swarm · SLAM",
    "Raffaello D'Andrea": "ETH Zürich · UAV Control · Acrobatics",
    "Shaojie Shen": "HKUST · Aerial Robotics · Autonomy",
    "Vijay Kumar": "UPenn · MAV · Swarm · Coordination",
    "Zhihong Liu": "NUDT · UAV Control · Formation",
    "Xiangke Wang": "NUDT · UAV Control · Formation",
    "Boyu Zhou": "SUSTech · UAV · Planning · SLAM",
    "Ángel Romero": "UZH · Agile Flight · Deep RL",
    "Yirui Cong": "NUDT · Multi-agent Systems · Estimation",
    "Huazhe Xu": "Embodied AI · Reinforcement Learning · Robotics",
    "Kaiming He": "Computer Vision · Representation Learning",
    "Guanzheng Wang": "UAV · Robotics · Autonomous Systems",
}

KNOWN_LINKS = {
    "Tairan He": {"scholar": "https://scholar.google.com.hk/citations?user=TVWH2U8AAAAJ&hl=zh-CN&oi=sra", "homepage": "https://tairanhe.com/", "github": "https://github.com/TairanHe"},
    "Chao Yan": {"scholar": "https://scholar.google.com.hk/citations?user=BUNXCTMAAAAJ&hl=zh-CN&oi=sra", "homepage": "https://ieeexplore.ieee.org/author/37086440285"},
    "Dario Floreano": {"scholar": "https://scholar.google.com.hk/citations?user=a5MoXOYAAAAJ&hl=zh-CN&oi=sra", "homepage": "https://www.epfl.ch/labs/lis/"},
    "Davide Scaramuzza": {"scholar": "https://scholar.google.com.hk/citations?user=SC9wV2kAAAAJ&hl=zh-CN&oi=sra", "homepage": "https://rpg.ifi.uzh.ch/", "github": "https://github.com/uzh-rpg"},
    "Fei Gao": {"scholar": "https://scholar.google.com.hk/citations?hl=zh-CN&user=4RObDv0AAAAJ", "homepage": "https://feigao-robotics.com/", "github": "https://github.com/ZJU-FAST-Lab"},
    "Raffaello D'Andrea": {"scholar": "https://scholar.google.com.hk/citations?user=FdGOel8AAAAJ&hl=zh-CN&oi=sra", "homepage": "https://raffaello.name/"},
    "Shaojie Shen": {"scholar": "https://scholar.google.com.hk/citations?user=u8Q0_xsAAAAJ&hl=zh-CN&oi=sra", "homepage": "https://seng.hkust.edu.hk/about/people/faculty/shaojie-shen", "github": "https://github.com/HKUST-Aerial-Robotics"},
    "Vijay Kumar": {"scholar": "https://scholar.google.com.hk/citations?hl=zh-CN&user=FUOEBDUAAAAJ", "homepage": "https://www.grasp.upenn.edu/people/vijay-kumar/", "github": "https://github.com/KumarRobotics"},
    "Zhihong Liu": {"scholar": "https://scholar.google.com.hk/citations?hl=zh-CN&user=zBhAyfkAAAAJ"},
    "Xiangke Wang": {"scholar": "https://scholar.google.com.hk/citations?user=WX3asHEAAAAJ&hl=zh-CN&oi=sra"},
    "Boyu Zhou": {"homepage": "https://mee.sustech.edu.cn/jiaozhiyuangong/3552.html"},
    "Ángel Romero": {"scholar": "https://scholar.google.com.hk/citations?hl=zh-CN&user=FF7T8EsAAAAJ"},
    "Yirui Cong": {"scholar": "https://scholar.google.com.hk/citations?hl=zh-CN&user=_gLig5MAAAAJ"},
}

CSS = """
:root{--bg:#0b1020;--panel:#121a2e;--panel2:#18233b;--text:#e7ecf6;--muted:#96a2b8;--line:#2a3856;--accent:#62a8ff;--good:#55d6a6}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top,#182744 0,var(--bg) 42%);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif;line-height:1.55;min-height:100vh}
a{color:inherit}.wrap{width:min(1180px,calc(100% - 36px));margin:auto}.top{padding:34px 0 25px;border-bottom:1px solid var(--line)}.crumbs{display:flex;gap:18px;flex-wrap:wrap}.crumbs a,.links a{color:var(--accent);text-decoration:none}.top h1{font-size:clamp(1.8rem,4vw,2.8rem);margin:18px 0 6px}.sub{color:var(--muted)}.links{display:flex;gap:14px;flex-wrap:wrap;margin-top:16px}.links a{border:1px solid var(--line);border-radius:999px;padding:6px 11px;background:#0d1528}
main{padding:28px 0 46px}.summary{display:flex;align-items:center;gap:12px;margin-bottom:22px;color:var(--muted)}.count{font-size:1.55rem;color:var(--accent);font-weight:750}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:15px}.card{display:block;text-decoration:none;padding:18px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(145deg,var(--panel),var(--panel2));min-height:150px;transition:.18s}.card:hover{transform:translateY(-2px);border-color:var(--accent);box-shadow:0 12px 32px #0005}.card h2{font-size:1rem;line-height:1.45;margin:10px 0}.meta{font-size:.78rem;color:var(--muted)}.badge{display:inline-block;color:var(--good);border:1px solid #55d6a655;border-radius:999px;padding:2px 8px;font-size:.72rem}.empty{padding:28px;border:1px dashed var(--line);border-radius:14px;color:var(--muted)}.assets{display:grid;gap:10px;margin-top:22px}.asset{display:flex;justify-content:space-between;gap:18px;padding:13px 15px;background:var(--panel);border:1px solid var(--line);border-radius:10px;text-decoration:none}.asset:hover{border-color:var(--accent)}footer{padding:24px 0 36px;color:var(--muted);border-top:1px solid var(--line);font-size:.82rem}@media(max-width:600px){.grid{grid-template-columns:1fr}.asset{display:block}}
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def scholar_dirs() -> list[Path]:
    return sorted((p for p in SCHOLARS.iterdir() if p.is_dir() and not p.name.startswith(".")), key=lambda p: p.name.casefold())


def normalize_layout() -> None:
    for scholar in scholar_dirs():
        nested = scholar / scholar.name
        if not nested.is_dir():
            continue
        for source in list(nested.iterdir()):
            target = scholar / source.name
            if target.exists():
                raise FileExistsError(f"Cannot flatten {source}: {target} already exists")
            shutil.move(str(source), str(target))
        nested.rmdir()


def read_links(scholar: Path) -> dict[str, str]:
    links = {key: "" for key in ("scholar", "homepage", "github")}
    links.update(KNOWN_LINKS.get(scholar.name, {}))
    for key, filename in (("scholar", "google_scholar.txt"), ("homepage", "homepage.txt"), ("github", "github.txt")):
        path = scholar / filename
        if path.is_file():
            value = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
            if value:
                links[key] = value[0].strip()
    return links


def rdf_metadata(scholar: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    namespaces = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "link": "http://purl.org/rss/1.0/modules/link/",
        "bib": "http://purl.org/net/biblio#",
        "foaf": "http://xmlns.com/foaf/0.1/",
    }
    for rdf in scholar.glob("*.rdf"):
        try:
            root = ET.parse(rdf).getroot()
        except ET.ParseError:
            continue
        # Zotero uses rdf:Description for some types and bib:Article,
        # bib:Thesis, bib:Book, etc. for others. All are direct children.
        for item in root:
            title = item.findtext("dc:title", default="", namespaces=namespaces).strip()
            if not title:
                continue
            item_ids = []
            for link in item.findall("link:link", namespaces):
                resource = link.get(f"{{{namespaces['rdf']}}}resource", "")
                match = re.fullmatch(r"#item_(.+)", resource)
                if match:
                    item_ids.append(match.group(1))
            if not item_ids:
                continue
            date = item.findtext("dc:date", default="", namespaces=namespaces).strip()
            if not date:
                date = item.findtext("dcterms:issued", default="", namespaces=namespaces).strip()
            authors = []
            for person in item.findall("bib:authors/rdf:Seq/rdf:li/foaf:Person", namespaces):
                given = person.findtext("foaf:givenName", default="", namespaces=namespaces).strip()
                surname = person.findtext("foaf:surname", default="", namespaces=namespaces).strip()
                name = " ".join(part for part in (given, surname) if part)
                if name:
                    authors.append(name)
            abstract = item.findtext("dcterms:abstract", default="", namespaces=namespaces).strip()
            source = item.get(f"{{{namespaces['rdf']}}}about", "")
            entry = {
                "title": title,
                "date": date,
                "authors": ", ".join(authors),
                "abstract": abstract,
                "source": source if source.startswith(("http://", "https://")) else "",
            }
            for item_id in item_ids:
                result[item_id] = entry.copy()
    return result


def paper_info(folder: Path, metadata: dict[str, dict[str, str]]) -> dict[str, object]:
    assets = sorted((p for p in folder.iterdir() if p.is_file() and p.name not in {"index.html", "note.html"}), key=lambda p: (p.suffix.lower() != ".pdf", p.name.casefold()))
    primary = next((p for p in assets if p.suffix.lower() == ".pdf"), assets[0] if assets else None)
    fallback = primary.stem if primary else f"Paper {folder.name}"
    fallback = re.sub(r"^.+?\s+-\s+((?:19|20)\d{2})\s+-\s+", "", fallback)
    fallback = fallback.replace("_", " ").strip()
    data = metadata.get(folder.name, {})
    title = data.get("title") or fallback
    date = data.get("date") or ""
    if not date:
        year = re.search(r"(?:19|20)\d{2}", primary.stem if primary else "")
        date = year.group(0) if year else "Local file"
    return {
        "folder": folder,
        "title": title,
        "date": date,
        "authors": data.get("authors", ""),
        "abstract": data.get("abstract", ""),
        "source": data.get("source", ""),
        "assets": assets,
        "has_note": (folder / "note.html").is_file(),
    }


def page(title: str, header: str, subtitle: str, body: str, crumbs: str, links: str = "") -> str:
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style></head>
<body><header class="top"><div class="wrap"><nav class="crumbs">{crumbs}</nav><h1>{header}</h1><div class="sub">{subtitle}</div>{links}</div></header>
<main class="wrap">{body}</main><footer><div class="wrap">UAV-Survey · Scholar Tracking</div></footer></body></html>
'''


def write_paper_index(scholar: Path, info: dict[str, object]) -> None:
    folder = info["folder"]
    if info["has_note"]:
        redirect = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=note.html"><title>{esc(info["title"])}</title></head><body><p>Redirecting to the paper notes: <a href="note.html">open note.html</a>.</p></body></html>\n'''
        (folder / "index.html").write_text(redirect, encoding="utf-8", newline="\n")
        return
    assets = info["assets"]
    rows: list[str] = []
    if info["has_note"]:
        rows.append('<a class="asset" href="note.html"><span>📝 Paper notes</span><span>Open notes →</span></a>')
    for asset in assets:
        size = asset.stat().st_size
        display_size = f"{size / 1024 / 1024:.1f} MB" if size >= 1024 * 1024 else f"{max(1, round(size / 1024))} KB"
        rows.append(f'<a class="asset" href="{esc(quote(asset.name))}"><span>{esc(asset.name)}</span><span>{display_size} · Open →</span></a>')
    if not rows:
        rows.append('<div class="empty">This paper directory currently has no local assets.</div>')
    authors = f'<p class="meta">{esc(info["authors"])}</p>' if info["authors"] else ""
    abstract = f'<p>{esc(info["abstract"])}</p>' if info["abstract"] else ""
    source = f'<div class="links"><a href="{esc(info["source"])}" target="_blank" rel="noopener">Publication source ↗</a></div>' if info["source"] else ""
    body = f'<div class="summary"><span class="badge">{esc(info["date"])}</span><span>Paper {esc(folder.name)}</span></div>{authors}{abstract}{source}<div class="assets">{"".join(rows)}</div>'
    content = page(
        str(info["title"]), esc(info["title"]), "Local paper entry",
        body,
        f'<a href="../../index.html">← {esc(scholar.name)}</a><a href="../../../../index.html">UAV-Survey</a>',
    )
    (folder / "index.html").write_text(content, encoding="utf-8", newline="\n")


def write_scholar_index(scholar: Path, papers: list[dict[str, object]]) -> None:
    cards = []
    for info in papers:
        folder = info["folder"]
        badge = '<span class="badge">Notes available</span>' if info["has_note"] else '<span class="meta">Local files</span>'
        cards.append(f'<a class="card" href="files/{esc(quote(folder.name))}/index.html"><div class="meta">{esc(info["date"])}</div><h2>{esc(info["title"])}</h2>{badge}</a>')
    listing = f'<div class="grid">{"".join(cards)}</div>' if cards else '<div class="empty">No local papers have been added yet.</div>'
    body = f'<div class="summary"><span class="count">{len(papers)}</span><span>tracked papers · each entry uses <code>files/&lt;paper&gt;/index.html</code></span></div>{listing}'
    links = read_links(scholar)
    link_html = "".join(f'<a href="{esc(url)}" target="_blank" rel="noopener">{label}</a>' for key, label in (("scholar", "Google Scholar"), ("homepage", "Homepage"), ("github", "GitHub")) if (url := links.get(key)))
    content = page(
        f"{scholar.name} · Scholar Dashboard", esc(scholar.name), esc(DESCRIPTIONS.get(scholar.name, "Research profile · Local paper library")),
        body,
        '<a href="../index.html">← All scholars</a><a href="../../index.html">UAV-Survey</a>',
        f'<div class="links">{link_html}</div>' if link_html else "",
    )
    (scholar / "index.html").write_text(content, encoding="utf-8", newline="\n")


def write_files_index(scholar: Path, papers: list[dict[str, object]]) -> None:
    files = scholar / "files"
    if not files.is_dir():
        return
    cards = []
    for info in papers:
        folder = info["folder"]
        badge = '<span class="badge">Notes available</span>' if info["has_note"] else '<span class="meta">Local files</span>'
        target = "note.html" if info["has_note"] else "index.html"
        cards.append(f'<a class="card" href="{esc(quote(folder.name))}/{target}"><div class="meta">{esc(info["date"])}</div><h2>{esc(info["title"])}</h2>{badge}</a>')
    listing = f'<div class="grid">{"".join(cards)}</div>' if cards else '<div class="empty">No local papers have been added yet.</div>'
    body = f'<div class="summary"><span class="count">{len(papers)}</span><span>paper directories</span></div>{listing}'
    content = page(
        f"{scholar.name} · Paper files", "Paper files", esc(scholar.name), body,
        f'<a href="../index.html">← {esc(scholar.name)}</a><a href="../../../index.html">UAV-Survey</a>',
    )
    (files / "index.html").write_text(content, encoding="utf-8", newline="\n")


def repair_note_backlinks(scholar: Path) -> None:
    files = scholar / "files"
    if not files.is_dir():
        return
    for note in files.glob("*/note.html"):
        content = note.read_text(encoding="utf-8", errors="strict")
        repaired = re.sub(r'href=(["\'])(?:\.\./){3,}index\.html\1', r'href=\1../../index.html\1', content)
        if repaired != content:
            note.write_text(repaired, encoding="utf-8", newline="\n")


def build_all() -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for scholar in scholar_dirs():
        metadata = rdf_metadata(scholar)
        files = scholar / "files"
        folders = sorted((p for p in files.iterdir() if p.is_dir()), key=lambda p: (not p.name.isdigit(), int(p.name) if p.name.isdigit() else p.name)) if files.is_dir() else []
        papers = [paper_info(folder, metadata) for folder in folders]
        for info in papers:
            write_paper_index(scholar, info)
        repair_note_backlinks(scholar)
        write_files_index(scholar, papers)
        summary.append({"path": scholar, "papers": papers, "links": read_links(scholar)})
    return summary


def write_root_index(summary: list[dict[str, object]]) -> None:
    cards = []
    total = 0
    for item in summary:
        scholar = item["path"]
        count = len(item["papers"])
        total += count
        cards.append(f'<a class="card" href="{esc(quote(scholar.name))}/index.html"><div class="meta">{esc(DESCRIPTIONS.get(scholar.name, "Research profile"))}</div><h2>{esc(scholar.name)}</h2><span class="badge">{count} papers</span></a>')
    body = f'<div class="summary"><span class="count">{len(summary)}</span><span>scholars · {total} local paper entries</span></div><div class="grid">{"".join(cards)}</div>'
    content = page("Scholar Tracking · UAV-Survey", "Scholar Tracking", "Normalized local research-paper library", body, '<a href="../index.html">← UAV-Survey home</a>')
    (SCHOLARS / "index.html").write_text(content, encoding="utf-8", newline="\n")


def patch_site_home(summary: list[dict[str, object]]) -> None:
    path = ROOT / "index.html"
    content = path.read_text(encoding="utf-8")
    entries = []
    for item in summary:
        scholar = item["path"]
        links = item["links"]
        entries.append({
            "name": scholar.name,
            "desc": DESCRIPTIONS.get(scholar.name, "Research profile · Local paper library"),
            "folder": f"2.Scholar/{scholar.name}/",
            "scholar": links.get("scholar", ""),
            "homepage": links.get("homepage", ""),
            "github": links.get("github", ""),
        })
    rendered = json.dumps(entries, ensure_ascii=False, indent=4)
    rendered = "\n".join("  " + line for line in rendered.splitlines())
    replacement = f"var scholars = {rendered.strip()};"
    content, count = re.subn(r"var scholars = \[.*?\n  \];", replacement, content, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not locate the scholars array in root index.html")
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    normalize_layout()
    summary = build_all()
    write_root_index(summary)
    patch_site_home(summary)
    # Scholar index pages are curated second-level dashboards. Preserve their
    # original navigation and only supplement newly added papers.
    from restore_scholar_navigation import main as restore_navigation
    restore_navigation()
    print(f"Rebuilt {len(summary)} scholar indexes and {sum(len(item['papers']) for item in summary)} paper indexes.")


if __name__ == "__main__":
    main()
