#!/usr/bin/env python3
"""
Weekly lab paper & news crawler for 0.Survey.
Uses arXiv API + Semantic Scholar API + lab website RSS/news scraping.

Sources:
  - arXiv API: export.arxiv.org/api/query
  - Semantic Scholar: api.semanticscholar.org/graph/v1/paper/search
  - Lab website RSS/HTML for news

Output per lab: papers.json, news.json
Output per survey topic: papers.json
Also generates a site-wide last_updated.json

Run: python crawl_labs.py          # quick crawl (last 30 days)
     python crawl_labs.py --days 90  # deep crawl
"""

import json
import os
import sys
import time
import hashlib
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Config ──
SCRIPT_DIR = Path(__file__).parent
CST = timezone(timedelta(hours=8))  # Beijing time
USER_AGENT = "0Survey-Crawler/1.0 (mailto:none)"
MAX_RESULTS_PER_QUERY = 15
REQUEST_DELAY = 1.5  # seconds between API calls (be polite)

# ── Lab definitions ──
LABS = [
    {
        "id": "ETH-ASL",
        "folder": "3.Lab/ETH-ASL",
        "arxiv_queries": [
            'au:Siegwart AND (all:drone OR all:UAV OR all:aerial OR all:MAV)',
            'all:"ETH Zurich" AND (all:autonomous AND all:drone)',
            'au:"Scaramuzza" AND all:event camera',
        ],
        "news_url": "https://asl.ethz.ch/news.html",
        "news_selector": "article, .news-item, .entry",
        "rss_url": None,
    },
    {
        "id": "UZH-RPG",
        "folder": "3.Lab/UZH-RPG",
        "arxiv_queries": [
            'au:Scaramuzza AND (all:drone OR all:event camera OR all:agile)',
            'all:"Robotics and Perception Group" AND all:UAV',
            'au:"Delmerico" AND all:drone',
        ],
        "news_url": "https://rpg.ifi.uzh.ch/news.html",
        "news_selector": "article, .news-item",
        "rss_url": None,
    },
    {
        "id": "UPenn-Kumar-GRASP",
        "folder": "3.Lab/UPenn-Kumar-GRASP",
        "arxiv_queries": [
            'au:"Vijay Kumar" AND (all:drone OR all:UAV OR all:MAV OR all:aerial)',
            'all:"GRASP Lab" AND (all:drone OR all:robot)',
            'au:"Pappas" AND all:multi-robot',
        ],
        "news_url": "https://www.grasp.upenn.edu/news/",
        "news_selector": "article, .post, .news-item",
        "rss_url": None,
    },
    {
        "id": "CMU-AirLab",
        "folder": "3.Lab/CMU-AirLab",
        "arxiv_queries": [
            'au:"Sebastian Scherer" AND (all:aerial OR all:drone OR all:UAV)',
            'all:"AirLab" AND (all:drone OR all:autonomous)',
            'all:"CMU" AND all:field AND all:robot AND all:aerial',
        ],
        "news_url": "https://theairlab.org/news/",
        "news_selector": "article, .post, .news-entry",
        "rss_url": "https://theairlab.org/feed/",
    },
    {
        "id": "MIT-ACL",
        "folder": "3.Lab/MIT-ACL",
        "arxiv_queries": [
            'au:"Jonathan How" AND (all:drone OR all:UAV OR all:multi-agent)',
            'all:"MIT" AND all:aerospace AND all:controls AND (all:drone OR all:UAV)',
        ],
        "news_url": "https://acl.mit.edu/news/",
        "news_selector": "article, .news-item, .post",
        "rss_url": None,
    },
    {
        "id": "TUDelft-MAVLab",
        "folder": "3.Lab/TUDelft-MAVLab",
        "arxiv_queries": [
            'au:"de Croon" AND (all:drone OR all:MAV OR all:bio-inspired)',
            'all:"MAVLab" AND (all:drone OR all:micro OR all:swarm)',
        ],
        "news_url": "https://mavlab.tudelft.nl/news/",
        "news_selector": "article, .news-item, .post",
        "rss_url": None,
    },
    {
        "id": "Imperial-ARL",
        "folder": "3.Lab/Imperial-ARL",
        "arxiv_queries": [
            'au:"Mirko Kovac" AND (all:aerial OR all:drone OR all:robot)',
            'all:"Imperial College" AND all:aerial AND all:robotics',
        ],
        "news_url": "https://www.imperial.ac.uk/aerial-robotics/news/",
        "news_selector": "article, .news-item, .entry",
        "rss_url": None,
    },
    {
        "id": "ZJU-FAST",
        "folder": "3.Lab/ZJU-FAST",
        "arxiv_queries": [
            'au:"Fei Gao" AND (all:drone OR all:trajectory OR all:UAV)',
            'all:"ZJU" AND all:FAST AND (all:drone OR all:swarm)',
            'all:"ego-planner" OR all:"FAST-LIO"',
        ],
        "news_url": "https://zju-fast-lab.github.io/",
        "news_selector": "article, .news, .post",
        "rss_url": None,
    },
    {
        "id": "BUAA-RFLY",
        "folder": "3.Lab/BUAA-RFLY",
        "arxiv_queries": [
            'all:"RflySim" OR all:"reliable flight control"',
            'all:"BUAA" AND (all:UAV OR all:flight OR all:drone) AND all:safety',
        ],
        "news_url": "https://rfly.buaa.edu.cn/",
        "news_selector": ".news, .post, article",
        "rss_url": None,
    },
]

# Survey topic queries
SURVEYS = [
    {
        "id": "Anti-UAV",
        "folder": "5.UAV Field/Anti-UAV",
        "arxiv_queries": [
            'all:counter-drone OR all:anti-UAV OR all:"counter unmanned"',
            'all:"drone detection" AND (all:radar OR all:RF OR all:acoustic)',
            'all:UAV AND all:neutralization AND all:defense',
        ],
    },
    {
        "id": "Swarm Intelligence",
        "folder": "5.UAV Field/Swarm Intelligence",
        "arxiv_queries": [
            'all:"swarm intelligence" AND all:UAV',
            'all:"particle swarm" OR all:"ant colony" AND all:drone',
            'all:"multi-agent" AND all:swarm AND all:coordination',
        ],
    },
    {
        "id": "UAV+RL",
        "folder": "5.UAV Field/UAV+RL",
        "arxiv_queries": [
            'all:"reinforcement learning" AND (all:UAV OR all:drone OR all:aerial)',
            'all:"deep reinforcement learning" AND all:multi-UAV',
            'all:"MARL" AND all:UAV AND all:cooperative',
        ],
    },
]


# ── Helpers ──
def log(msg):
    ts = datetime.now(CST).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def fetch_url(url, retries=3):
    """Fetch URL with retries and delay."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limit
                wait = 10 * (i + 1)
                log(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            log(f"  HTTP {e.code} for {url[:80]}")
            return None
        except Exception as e:
            if i < retries - 1:
                time.sleep(2)
                continue
            log(f"  Error fetching {url[:80]}: {e}")
            return None
    return None


def search_arxiv(query, max_results=MAX_RESULTS_PER_QUERY, days_back=90):
    """Search arXiv API, return list of paper dicts."""
    # Build date filter
    today = datetime.now(timezone.utc)
    date_from = (today - timedelta(days=days_back)).strftime("%Y%m%d")
    date_to = today.strftime("%Y%m%d")

    encoded_query = urllib.parse.quote(query)
    url = (
        f"https://export.arxiv.org/api/query?"
        f"search_query={encoded_query}&start=0&max_results={max_results}&"
        f"sortBy=submittedDate&sortOrder=descending"
    )

    xml_str = fetch_url(url)
    if not xml_str:
        return []

    papers = []
    try:
        root = ET.fromstring(xml_str)
        ns = {"a": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("a:entry", ns):
            title_el = entry.find("a:title", ns)
            title = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"
            # Clean up newlines in title
            title = " ".join(title.split())

            authors = []
            for author in entry.findall("a:author", ns):
                name_el = author.find("a:name", ns)
                if name_el is not None and name_el.text:
                    authors.append(name_el.text.strip())

            published_el = entry.find("a:published", ns)
            published = published_el.text.strip()[:10] if published_el is not None and published_el.text else ""

            id_el = entry.find("a:id", ns)
            arxiv_id = ""
            paper_url = ""
            if id_el is not None and id_el.text:
                full_id = id_el.text.strip()
                arxiv_id = full_id.split("/abs/")[-1]
                paper_url = full_id

            summary_el = entry.find("a:summary", ns)
            summary = summary_el.text.strip()[:300] if summary_el is not None and summary_el.text else ""

            # Journal reference from arXiv metadata
            journal_ref_el = entry.find("a:journal_ref", ns)
            journal_ref = journal_ref_el.text.strip() if journal_ref_el is not None and journal_ref_el.text else ""

            papers.append({
                "title": title,
                "authors": ", ".join(authors[:8]),
                "year": published[:4] if published else "",
                "date": published,
                "arxiv_id": arxiv_id if not arxiv_id.startswith("http") else "",
                "url": paper_url if not paper_url.startswith("http://arxiv.org/abs/http") else paper_url.replace("http://arxiv.org/abs/http://", "http://"),
                "summary": summary,
                "source": "arxiv",
                "journal_ref": journal_ref,
                "citations": 0,
            })
    except ET.ParseError as e:
        log(f"  XML parse error: {e}")
        return []

    return papers


def search_semantic_scholar(query, max_results=10):
    """Search Semantic Scholar API (free tier, no key needed for low volume)."""
    encoded = urllib.parse.quote(query)
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/search?"
        f"query={encoded}&limit={max_results}&"
        f"fields=title,authors,year,externalIds,url,publicationDate"
    )

    data_str = fetch_url(url)
    if not data_str:
        return []

    try:
        data = json.loads(data_str)
        papers = []
        for item in data.get("data", []):
            authors = [a.get("name", "") for a in item.get("authors", [])]
            arxiv_id = ""
            ext_ids = item.get("externalIds", {}) or {}
            if "ArXiv" in ext_ids:
                arxiv_id = ext_ids["ArXiv"]

            papers.append({
                "title": item.get("title", "Untitled"),
                "authors": ", ".join(authors[:8]),
                "year": str(item.get("year", "")),
                "date": item.get("publicationDate", ""),
                "arxiv_id": arxiv_id,
                "url": item.get("url", "") or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""),
                "summary": "",
                "source": "semantic_scholar",
                "citations": item.get("citationCount", 0) or 0,
            })
        return papers
    except json.JSONDecodeError:
        return []


def scrape_news_from_html(html, selector_hint):
    """Very basic news scraping from HTML. Tries to find <article>, <li>, or generic items."""
    items = []
    # Simple pattern matching for common news structures
    import re

    # Try to find <article> tags
    article_pattern = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not article_pattern:
        # Try list items with links + dates
        article_pattern = re.findall(r'<li[^>]*class="[^"]*news[^"]*"[^>]*>(.*?)</li>', html, re.DOTALL)
    if not article_pattern:
        # Try generic divs with news class
        article_pattern = re.findall(r'<div[^>]*class="[^"]*(?:news|post|entry)[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)

    for block in article_pattern[:10]:
        # Extract link
        link_match = re.search(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', block, re.DOTALL)
        if not link_match:
            continue
        url = link_match.group(1)
        title = re.sub(r'<[^>]+>', '', link_match.group(2)).strip()
        if not title or len(title) < 5:
            continue

        # Try to extract date
        date_match = re.search(r'(?:<time[^>]*>|datetime="([^"]*)")?(?:(\d{4}-\d{2}-\d{2})|(\d{2}\.\d{2}\.\d{4}))', block)
        date_str = ""
        if date_match:
            for g in date_match.groups():
                if g:
                    date_str = g[:10]
                    break

        items.append({
            "title": title[:200],
            "url": url if url.startswith("http") else "",
            "date": date_str,
        })

    return items


def scrape_rss(rss_url):
    """Parse RSS/Atom feed for news items."""
    xml_str = fetch_url(rss_url)
    if not xml_str:
        return []

    items = []
    try:
        root = ET.fromstring(xml_str)

        # Try Atom first
        ns_atom = "http://www.w3.org/2005/Atom"
        entries = root.findall(f"{{{ns_atom}}}entry")
        if entries:
            for entry in entries[:10]:
                title_el = entry.find(f"{{{ns_atom}}}title")
                link_el = entry.find(f"{{{ns_atom}}}link")
                updated_el = entry.find(f"{{{ns_atom}}}updated")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                url = link_el.get("href", "") if link_el is not None else ""
                date = updated_el.text[:10] if updated_el is not None and updated_el.text else ""

                if title:
                    items.append({"title": title[:200], "url": url, "date": date})
            return items

        # Try RSS 2.0
        for item in root.iter("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            date_el = item.find("pubDate")

            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            url = link_el.text.strip() if link_el is not None and link_el.text else ""
            date = date_el.text.strip()[:10] if date_el is not None and date_el.text else ""

            if title:
                items.append({"title": title[:200], "url": url, "date": date})
    except ET.ParseError:
        pass

    return items[:10]


def deduplicate_papers(papers):
    """Remove duplicates by title similarity / arxiv_id."""
    seen = set()
    unique = []
    for p in papers:
        key = p.get("arxiv_id") or hashlib.md5(p["title"].lower().encode()).hexdigest()[:12]
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def load_journal_metrics():
    """Load journal quality database."""
    metrics_path = SCRIPT_DIR / "journal_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f).get("journals", {})
    return {}


def match_journal(title, arxiv_journal_ref, journal_db):
    """Match a paper to a known journal/conference. Returns (name, metrics) or (None, None)."""
    # 1. Check arXiv journal reference first
    if arxiv_journal_ref:
        ref_lower = arxiv_journal_ref.lower()
        for jname, metrics in journal_db.items():
            if jname.lower() in ref_lower:
                return jname, metrics
            for alias in metrics.get("aliases", []):
                if alias.lower() in ref_lower:
                    return jname, metrics

    # 2. Check title for conference abbreviations (e.g. "NeurIPS 2025")
    if title:
        for jname, metrics in journal_db.items():
            if metrics.get("type") == "conference" and jname.lower() in title.lower():
                return jname, metrics

    return None, None


def enrich_papers(papers, journal_db):
    """Add journal quality metrics and format fields for display."""
    for p in papers:
        # Journal matching
        arxiv_ref = p.get("journal_ref", "")
        jname, jmetrics = match_journal(p.get("title", ""), arxiv_ref, journal_db)
        if jmetrics:
            p["journal"] = jname
            p["journal_if"] = jmetrics.get("if")
            p["journal_cas"] = jmetrics.get("cas")
            p["journal_ccf"] = jmetrics.get("ccf")
            p["journal_type"] = jmetrics.get("type", "journal")
            p["journal_publisher"] = jmetrics.get("publisher")
            p["journal_full_name"] = jmetrics.get("full_name", jname)

        # Add quality badge
        badges = []
        if p.get("journal_ccf"):
            badges.append(f"CCF-{p['journal_ccf']}")
        if p.get("journal_cas"):
            badges.append(f"CAS {p['journal_cas']}")
        if p.get("journal_if"):
            badges.append(f"IF {p['journal_if']}")
        p["quality_badges"] = badges
        p["quality_score"] = compute_quality_score(p)

    return papers


def compute_quality_score(paper):
    """Compute a 0-10 quality score based on venue and citations."""
    score = 0
    # CCF rank
    ccf_scores = {"A": 4, "B": 2.5, "C": 1}
    score += ccf_scores.get(paper.get("journal_ccf"), 0)
    # CAS quartile
    cas_scores = {"Q1": 3, "Q2": 1.5, "Q3": 0.5}
    score += cas_scores.get(paper.get("journal_cas"), 0)
    # Impact factor contribution (capped)
    if_val = paper.get("journal_if") or 0
    score += min(if_val / 5, 3)  # max 3 points from IF
    # Citation bonus
    citations = paper.get("citations", 0)
    if citations >= 100:
        score += 1
    elif citations >= 10:
        score += 0.5
    return round(min(score, 10), 1)


# ── Main crawl logic ──
def crawl_lab(lab, days_back):
    """Crawl papers and news for one lab."""
    log(f"Crawling {lab['id']}...")

    all_papers = []

    # arXiv queries
    for q in lab.get("arxiv_queries", []):
        log(f"  arXiv: {q[:80]}...")
        papers = search_arxiv(q, max_results=MAX_RESULTS_PER_QUERY, days_back=days_back)
        all_papers.extend(papers)
        time.sleep(REQUEST_DELAY)

    # Semantic Scholar (complementary, for broader coverage)
    for q in lab.get("arxiv_queries", [])[:1]:  # just use first query for S2
        log(f"  Semantic Scholar: {q[:60]}...")
        papers = search_semantic_scholar(q, max_results=8)
        # Only add if not already in list
        existing_titles = {p["title"].lower() for p in all_papers}
        for p in papers:
            if p["title"].lower() not in existing_titles:
                all_papers.append(p)
        time.sleep(REQUEST_DELAY)

    # Deduplicate
    all_papers = deduplicate_papers(all_papers)
    log(f"  Found {len(all_papers)} unique papers")

    # Enrich with journal metrics
    journal_db = load_journal_metrics()
    all_papers = enrich_papers(all_papers, journal_db)

    # Sort by recency
    all_papers.sort(key=lambda p: p.get("date", ""), reverse=True)

    # News
    news = []
    rss_url = lab.get("rss_url")
    if rss_url:
        log(f"  RSS: {rss_url}")
        news = scrape_rss(rss_url)
    elif lab.get("news_url"):
        log(f"  Scraping news: {lab['news_url'][:80]}")
        html = fetch_url(lab["news_url"])
        if html:
            news = scrape_news_from_html(html, lab.get("news_selector", ""))
            if not news:
                news = [
                    {"title": f"📄 New paper: {p['title'][:100]}", "url": p["url"], "date": p.get("date", "")}
                    for p in all_papers[:5]
                ]

    log(f"  Found {len(news)} news items")

    return all_papers, news


def crawl_survey(survey, days_back):
    """Crawl papers for a survey topic."""
    log(f"Crawling survey: {survey['id']}...")
    all_papers = []

    for q in survey.get("arxiv_queries", []):
        log(f"  arXiv: {q[:100]}...")
        papers = search_arxiv(q, max_results=MAX_RESULTS_PER_QUERY, days_back=days_back)
        all_papers.extend(papers)
        time.sleep(REQUEST_DELAY)

    all_papers = deduplicate_papers(all_papers)
    journal_db = load_journal_metrics()
    all_papers = enrich_papers(all_papers, journal_db)
    all_papers.sort(key=lambda p: p.get("date", ""), reverse=True)
    log(f"  Found {len(all_papers)} papers")
    return all_papers


def save_json(data, folder, filename):
    """Save JSON data to file, creating directory if needed."""
    path = SCRIPT_DIR / folder
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / filename
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"  Saved {filepath}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl lab papers and news")
    parser.add_argument("--days", type=int, default=30, help="Days back to search (default: 30)")
    parser.add_argument("--quick", action="store_true", help="Quick mode: 7 days, fewer results")
    args = parser.parse_args()

    days = 7 if args.quick else args.days
    log(f"=== 0.Survey Crawler ===")
    log(f"Searching {days} days back")
    log(f"Labs: {len(LABS)}, Surveys: {len(SURVEYS)}")
    log("")

    all_updates = {}

    # Crawl labs
    for lab in LABS:
        papers, news = crawl_lab(lab, days)
        save_json(papers, lab["folder"], "papers.json")
        save_json(news, lab["folder"], "news.json")
        all_updates[lab["id"]] = {
            "papers_count": len(papers),
            "news_count": len(news),
            "last_crawl": datetime.now(CST).isoformat(),
        }
        log("")

    # Crawl surveys
    for survey in SURVEYS:
        papers = crawl_survey(survey, days)
        save_json(papers, survey["folder"], "papers.json")
        all_updates[survey["id"]] = {
            "papers_count": len(papers),
            "last_crawl": datetime.now(CST).isoformat(),
        }
        log("")

    # Save global status
    status = {
        "last_updated": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST"),
        "days_searched": days,
        "labs": all_updates,
    }
    save_json(status, ".", "last_updated.json")
    log("=== Done ===")


if __name__ == "__main__":
    main()
