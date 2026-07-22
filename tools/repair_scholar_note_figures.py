#!/usr/bin/env python3
"""Fill missing note figure assets with source-grounded PDF page snapshots."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SCHOLARS = ROOT / "2.Scholar"


def page_for_figure(page_texts: list[str], number: int) -> int | None:
    pattern = re.compile(rf"(?:\bFig(?:ure)?\.?\s*{number}\b|图\s*{number}\b)", re.I)
    for index, text in enumerate(page_texts):
        if pattern.search(text):
            return index
    figure_pages = [index for index, text in enumerate(page_texts) if re.search(r"(?:\bFig(?:ure)?\.?\s*\d+|图\s*\d+)", text, re.I)]
    if figure_pages:
        return figure_pages[min(number - 1, len(figure_pages) - 1)]
    return None


def repair_note(note: Path) -> tuple[str, int, bool, str]:
    folder = note.parent
    content = note.read_text(encoding="utf-8", errors="strict")
    referenced = sorted(set(re.findall(r'(?:src|href)=["\']figures/fig(\d+)\.png["\']', content)), key=int)
    missing_numbers = [int(number) for number in referenced if not (folder / "figures" / f"fig{number}.png").is_file()]
    needs_section = not re.search(r'<section\s+id=["\']figures["\']', content)
    pdf = next(folder.glob("*.pdf"), None)
    created = 0
    generated_numbers: list[int] = []
    if pdf and (missing_numbers or needs_section):
        try:
            reader = PdfReader(str(pdf))
            page_texts = [page.extract_text() or "" for page in reader.pages]
            requested = missing_numbers[:]
            if needs_section and not requested:
                seen_pages = []
                for number in range(1, 4):
                    page_index = page_for_figure(page_texts, number)
                    if page_index is not None and page_index not in seen_pages:
                        requested.append(number)
                        seen_pages.append(page_index)
            render_jobs = []
            for number in requested:
                page_index = page_for_figure(page_texts, number)
                if page_index is not None:
                    render_jobs.append((number, page_index))
            with pdfplumber.open(pdf) as document:
                (folder / "figures").mkdir(exist_ok=True)
                for number, page_index in render_jobs:
                    target = folder / "figures" / f"fig{number}.png"
                    document.pages[page_index].to_image(resolution=120).save(target)
                    created += 1
                    generated_numbers.append(number)
        except Exception as exc:
            return (str(note.relative_to(ROOT)), created, needs_section, str(exc))
    if needs_section:
        images = "".join(
            f'<div class="paper-figure"><div class="fig-header"><span class="fig-number">Source figure {number}</span><span class="fig-caption">Local PDF page containing the cited figure</span></div><div class="fig-image"><img src="figures/fig{number}.png" alt="Source figure {number}"></div><div class="fig-interpretation"><p>该图页直接从本地 PDF 渲染；精确图号、图注和变量含义请对照原文。</p></div></div>'
            for number in generated_numbers
        )
        if not images:
            images = '<div class="callout warn">当前 PDF 未能可靠定位独立图页；本节保留为原文图表核对入口，不虚构图像内容。</div>'
        section = f'<section id="figures"><h2>8. Paper Figures - 图表核对</h2>{images}</section>\n'
        flaw = re.search(r'<section\s+id=["\']flaw["\']', content)
        if flaw:
            content = content[:flaw.start()] + section + content[flaw.start():]
        else:
            content = content.replace("</main>", section + "</main>", 1)
        if 'href="#figures"' not in content:
            content = content.replace('<a href="#flaw">', '<a href="#figures">Figures</a><a href="#flaw">', 1)
        note.write_text(content, encoding="utf-8", newline="\n")
    return (str(note.relative_to(ROOT)), created, needs_section, "")


def main() -> None:
    notes = list(SCHOLARS.glob("*/files/*/note.html"))
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(repair_note, note): note for note in notes}
        for future in as_completed(futures):
            results.append(future.result())
    created = sum(item[1] for item in results)
    sections = sum(item[2] for item in results)
    errors = [item for item in results if item[3]]
    print(f"Checked {len(results)} notes; created {created} figure snapshots; added {sections} figure sections; errors={len(errors)}")
    for path, _, _, error in errors:
        print(f"ERROR {path}: {error}")


if __name__ == "__main__":
    main()
