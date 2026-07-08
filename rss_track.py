#!/usr/bin/env python3
"""
Collect paper candidates from arXiv/RSS feeds into a review inbox.

The tracker stores metadata only. It does not download PDFs, so the GitHub
repository stays small while still keeping a fresh paper discovery queue.
"""

from __future__ import annotations

import argparse
import email.utils
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG = SCRIPT_DIR / "feeds.json"
USER_AGENT = "UAV-Survey-RSS-Tracker/1.0"


ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def norm_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_xml(url: str, timeout: int = 30) -> ET.Element:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return ET.fromstring(resp.read())


def arxiv_url(query: str, max_results: int) -> str:
    params = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    return f"http://export.arxiv.org/api/query?{params}"


def parse_arxiv_entry(entry: ET.Element, feed: dict) -> dict:
    entry_id = norm_text(entry.findtext("atom:id", namespaces=ATOM_NS))
    arxiv_id = entry_id.split("/abs/")[-1] if "/abs/" in entry_id else entry_id.rsplit("/", 1)[-1]
    authors = [
        norm_text(author.findtext("atom:name", namespaces=ATOM_NS))
        for author in entry.findall("atom:author", ATOM_NS)
    ]
    published = norm_text(entry.findtext("atom:published", namespaces=ATOM_NS))[:10]
    pdf_url = ""
    for link in entry.findall("atom:link", ATOM_NS):
        if link.attrib.get("title") == "pdf":
            pdf_url = link.attrib.get("href", "")
            break

    return {
        "id": f"arxiv:{arxiv_id}",
        "title": norm_text(entry.findtext("atom:title", namespaces=ATOM_NS)),
        "authors": authors,
        "date": published,
        "year": published[:4] if published else "",
        "arxiv_id": arxiv_id,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": pdf_url,
        "summary": norm_text(entry.findtext("atom:summary", namespaces=ATOM_NS)),
        "source": "arxiv",
        "feed": feed["name"],
        "target": feed.get("target", ""),
    }


def parse_rss_date(raw: str) -> str:
    if not raw:
        return ""
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
        return parsed.date().isoformat()
    except Exception:
        return raw[:10]


def parse_rss_item(item: ET.Element, feed: dict) -> dict:
    guid = norm_text(item.findtext("guid")) or norm_text(item.findtext("link"))
    return {
        "id": f"rss:{guid}",
        "title": norm_text(item.findtext("title")),
        "authors": [],
        "date": parse_rss_date(norm_text(item.findtext("pubDate"))),
        "year": parse_rss_date(norm_text(item.findtext("pubDate")))[:4],
        "arxiv_id": "",
        "url": norm_text(item.findtext("link")),
        "pdf_url": "",
        "summary": norm_text(item.findtext("description")),
        "source": "rss",
        "feed": feed["name"],
        "target": feed.get("target", ""),
    }


def collect_feed(feed: dict, max_items: int) -> list[dict]:
    feed_type = feed.get("type", "rss").lower()
    if feed_type == "arxiv":
        root = fetch_xml(arxiv_url(feed["query"], max_items))
        return [parse_arxiv_entry(entry, feed) for entry in root.findall("atom:entry", ATOM_NS)]

    root = fetch_xml(feed["url"])
    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else root.findall(".//item")
    return [parse_rss_item(item, feed) for item in items[:max_items]]


def score_candidate(candidate: dict, feed: dict) -> tuple[float, list[str]]:
    haystack = " ".join(
        [
            candidate.get("title", ""),
            candidate.get("summary", ""),
            " ".join(candidate.get("authors", [])),
        ]
    ).lower()

    include_hits = [kw for kw in feed.get("include_keywords", []) if kw.lower() in haystack]
    exclude_hits = [kw for kw in feed.get("exclude_keywords", []) if kw.lower() in haystack]

    score = min(1.0, 0.12 * len(include_hits))
    if candidate.get("arxiv_id"):
        score += 0.08
    score -= 0.18 * len(exclude_hits)
    score = max(0.0, min(1.0, round(score, 2)))

    reasons = [f"matched: {', '.join(include_hits[:6])}"] if include_hits else []
    if exclude_hits:
        reasons.append(f"penalized: {', '.join(exclude_hits[:4])}")
    return score, reasons


def is_recent(candidate: dict, days: int) -> bool:
    if days <= 0 or not candidate.get("date"):
        return True
    try:
        date = datetime.fromisoformat(candidate["date"]).replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return date >= datetime.now(timezone.utc) - timedelta(days=days)


def merge_candidates(existing: list[dict], incoming: list[dict]) -> list[dict]:
    merged = {item.get("id") or item.get("url"): item for item in existing}
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    for item in incoming:
        key = item.get("id") or item.get("url")
        previous = merged.get(key, {})
        item["status"] = previous.get("status", "candidate")
        item["decision"] = previous.get("decision", "pending")
        item["notes"] = previous.get("notes", "")
        item["first_seen"] = previous.get("first_seen", now)
        item["last_seen"] = now
        merged[key] = {**previous, **item}

    return sorted(
        merged.values(),
        key=lambda item: (item.get("date", ""), item.get("relevance_score", 0)),
        reverse=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect RSS/arXiv paper candidates.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to feeds.json")
    parser.add_argument("--days", type=int, default=14, help="Only keep new results from this many days; use 0 for all")
    parser.add_argument("--output", help="Override output path")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing the inbox")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_json(config_path, {})
    if not config.get("feeds"):
        print(f"[ERROR] No feeds configured in {config_path}", file=sys.stderr)
        return 2

    output = Path(args.output or config.get("output", "other/inbox/papers_pending.json"))
    if not output.is_absolute():
        output = SCRIPT_DIR / output

    max_items = int(config.get("max_items_per_feed", 30))
    min_score = float(config.get("min_relevance_score", 0.25))
    collected = []

    for feed in config["feeds"]:
        print(f"[feed] {feed['name']}")
        try:
            candidates = collect_feed(feed, max_items)
        except Exception as exc:
            print(f"  [WARN] failed: {exc}", file=sys.stderr)
            continue

        kept = 0
        for candidate in candidates:
            if not is_recent(candidate, args.days):
                continue
            score, reasons = score_candidate(candidate, feed)
            if score < min_score:
                continue
            candidate["relevance_score"] = score
            candidate["reason"] = "; ".join(reasons) or "matched feed query"
            collected.append(candidate)
            kept += 1
        print(f"  kept {kept}/{len(candidates)} candidates")
        time.sleep(3.0 if feed.get("type") == "arxiv" else 0.5)

    existing = load_json(output, [])
    merged = merge_candidates(existing, collected)

    if args.dry_run:
        print(f"\n[dry-run] {len(collected)} new/seen candidates, {len(merged)} total in inbox")
        for item in collected[:10]:
            print(f"- [{item['feed']}] {item['date']} {item['title']} ({item['relevance_score']})")
        return 0

    save_json(output, merged)
    print(f"\n[OK] saved {len(merged)} candidates to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
