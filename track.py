#!/usr/bin/env python3
"""
Research Tracker — Automated monitoring of college teams & companies.
Run periodically (weekly recommended) to check for new publications & updates.

Usage:
    python track.py                    # Full report
    python track.py --arxiv            # arXiv only
    python track.py --github           # GitHub only
    python track.py --output report.md # Save to file
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
DEFAULT_LOOKBACK = 14

# Labs to track — add more as needed
LABS = {
    "ETH-ASL": {
        "arxiv_keywords": ["ETH Zurich", "autonomous systems lab", "siegwart"],
        "github_orgs": ["ethz-asl"],
        "github_repos": [],
    },
    "UZH-RPG": {
        "arxiv_keywords": ["scaramuzza", "event camera", "rpg", "UZH"],
        "github_orgs": ["uzh-rpg"],
        "github_repos": [],
    },
    "UPenn-Kumar": {
        "arxiv_keywords": ["vijay kumar", "GRASP lab", "UPenn aerial"],
        "github_orgs": ["KumarRobotics"],
        "github_repos": [],
    },
    "CMU-AirLab": {
        "arxiv_keywords": ["sebastian scherer", "airlab", "CMU aerial"],
        "github_orgs": ["castacks"],
        "github_repos": [],
    },
    "MIT-ACL": {
        "arxiv_keywords": ["jonathan how", "MIT aerospace controls", "acl mit"],
        "github_orgs": ["mit-acl"],
        "github_repos": [],
    },
    "TUDelft-MAVLab": {
        "arxiv_keywords": ["guido de croon", "MAVLab", "TU Delft drone"],
        "github_orgs": ["tudelft"],
        "github_repos": [],
    },
    "Imperial-ARL": {
        "arxiv_keywords": ["mirko kovac", "aerial robotics imperial"],
        "github_orgs": [],
        "github_repos": [],
    },
    "ZJU-FAST": {
        "arxiv_keywords": ["fei gao", "ZJU FAST", "trajectory planning drone", "ego-planner"],
        "github_orgs": ["ZJU-FAST-Lab"],
        "github_repos": ["ZJU-FAST-Lab/ego-planner-v2", "ZJU-FAST-Lab/FAST-LIO"],
    },
    "BUAA-RFLY": {
        "arxiv_keywords": ["BUAA reliable flight", "RflySim", "reliable flight control"],
        "github_orgs": [],
        "github_repos": [],
    },
}

COMPANIES = {
    "Unitree": {
        "arxiv_keywords": ["unitree", "H1 humanoid", "quadruped locomotion"],
        "github_orgs": ["unitreerobotics"],
        "github_repos": [],
    },
}

MAX_RESULTS = 20


# ── arXiv API ──────────────────────────────────────────────────────────────

def search_arxiv(query: str, max_results: int = 10) -> list[dict]:
    """Search arXiv API and return list of paper dicts."""
    base_url = "http://export.arxiv.org/api/query"
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{base_url}?{params}"

    papers = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchTracker/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        root = ET.fromstring(data)

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            published = entry.find("atom:published", ns)
            arxiv_id_elem = entry.find("atom:id", ns)

            authors = [
                author.find("atom:name", ns).text.strip()
                for author in entry.findall("atom:author", ns)
            ]

            arxiv_id = ""
            if arxiv_id_elem is not None:
                arxiv_id = arxiv_id_elem.text.strip().split("/abs/")[-1]

            papers.append({
                "title": title.text.strip().replace("\n", " ") if title is not None else "N/A",
                "authors": authors,
                "published": published.text.strip()[:10] if published is not None else "N/A",
                "arxiv_id": arxiv_id,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "summary": summary.text.strip()[:300] if summary is not None else "",
            })
    except Exception as e:
        print(f"  [WARN] arXiv query failed for '{query}': {e}", file=sys.stderr)

    return papers


# ── GitHub API ─────────────────────────────────────────────────────────────

def get_github_events(owner: str, repo: str | None = None, lookback_days: int = 14) -> list[dict]:
    """Get recent events for a GitHub org/user or repo."""
    headers = {
        "User-Agent": "ResearchTracker/1.0",
        "Accept": "application/vnd.github+json",
    }
    # Use token if available for higher rate limits
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if repo:
        url = f"https://api.github.com/repos/{repo}/events?per_page=10"
    else:
        url = f"https://api.github.com/orgs/{owner}/events?per_page=10"

    events = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
        for evt in data:
            created = datetime.fromisoformat(evt["created_at"].replace("Z", "+00:00"))
            if created > cutoff:
                events.append({
                    "type": evt["type"],
                    "repo": evt.get("repo", {}).get("name", "N/A"),
                    "created_at": evt["created_at"],
                    "action": evt.get("payload", {}).get("action", ""),
                })
    except Exception as e:
        print(f"  [WARN] GitHub API failed for '{owner}/{repo or ''}': {e}", file=sys.stderr)

    return events


# ── Report Generation ──────────────────────────────────────────────────────

def generate_report(arxiv_results: dict, github_results: dict, lookback_days: int = 14) -> str:
    """Generate a markdown report from collected results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Research Tracking Report",
        f"Generated: {now}",
        f"Lookback: {lookback_days} days\n",
    ]

    # arXiv section
    lines.append("---\n## [arxiv] arXiv - Recent Papers\n")

    total_papers = 0
    for lab, papers in arxiv_results.items():
        if papers:
            lines.append(f"### {lab} ({len(papers)} papers)\n")
            for p in papers[:5]:
                authors_short = ", ".join(p["authors"][:3])
                if len(p["authors"]) > 3:
                    authors_short += " et al."
                lines.append(f"- **[{p['title']}]({p['url']})**")
                lines.append(f"  - {authors_short} -- {p['published']}")
                lines.append(f"  - `arxiv:{p['arxiv_id']}`")
            lines.append("")
            total_papers += len(papers)

    if total_papers == 0:
        lines.append("*No new papers found in the lookback period.*\n")

    # GitHub section
    lines.append("---\n## [github] GitHub — Recent Activity\n")

    total_events = 0
    for lab, events in github_results.items():
        if events:
            lines.append(f"### {lab}\n")
            for e in events[:10]:
                icon = {"PushEvent": "[push]", "PullRequestEvent": "[pr]", "IssuesEvent": "[issue]",
                         "ReleaseEvent": "[release]", "CreateEvent": "[create]", "ForkEvent": "[fork]",
                         "WatchEvent": "[star]", "DeleteEvent": "[delete]"}.get(e["type"], "[event]")
                lines.append(f"- {icon} **{e['repo']}**: {e['type']} ({e.get('action', '')}) -- {e['created_at'][:10]}")
            lines.append("")
            total_events += len(events)

    if total_events == 0:
        lines.append("*No recent GitHub activity found.*\n")

    lines.append("---\n")
    lines.append(f"*Report auto-generated by track.py. Run `python track.py --help` for options.*")

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Research Tracker")
    parser.add_argument("--arxiv", action="store_true", help="arXiv only")
    parser.add_argument("--github", action="store_true", help="GitHub only")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--days", type=int, default=DEFAULT_LOOKBACK, help=f"Days to look back (default: {DEFAULT_LOOKBACK})")
    parser.add_argument("--cache", type=str, default=str(SCRIPT_DIR / ".track_cache.json"), help="Cache file path")
    args = parser.parse_args()

    lookback_days = args.days
    all_targets = {**LABS, **COMPANIES}
    run_arxiv = args.arxiv or not (args.arxiv or args.github)
    run_github = args.github or not (args.arxiv or args.github)

    arxiv_results = {}
    github_results = {}

    if run_arxiv:
        print("=" * 60)
        print("[arxiv] Querying arXiv API...")
        print("=" * 60)
        for name, cfg in all_targets.items():
            if not cfg["arxiv_keywords"]:
                continue
            print(f"\n  {name}...")
            papers = []
            seen_ids = set()
            for kw in cfg["arxiv_keywords"]:
                results = search_arxiv(kw, max_results=MAX_RESULTS)
                for p in results:
                    if p["arxiv_id"] not in seen_ids:
                        seen_ids.add(p["arxiv_id"])
                        papers.append(p)
                time.sleep(3.0)  # Rate limiting (arXiv requires >1s between requests)

            papers.sort(key=lambda p: p["published"], reverse=True)
            arxiv_results[name] = papers[:MAX_RESULTS]
            print(f"    Found {len(papers)} papers (showing top {min(len(papers), MAX_RESULTS)})")

    if run_github:
        print("\n" + "=" * 60)
        print("[github] Querying GitHub API...")
        print("=" * 60)
        for name, cfg in all_targets.items():
            if not cfg["github_orgs"] and not cfg["github_repos"]:
                continue
            print(f"\n  {name}...")
            events = []
            for org in cfg["github_orgs"]:
                events.extend(get_github_events(org, lookback_days=lookback_days))
                time.sleep(0.3)
            for repo in cfg["github_repos"]:
                events.extend(get_github_events(None, repo, lookback_days=lookback_days))
                time.sleep(0.3)

            events.sort(key=lambda e: e["created_at"], reverse=True)
            github_results[name] = events
            print(f"    Found {len(events)} events in last {lookback_days} days")

    report = generate_report(arxiv_results, github_results, lookback_days=lookback_days)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(report, encoding="utf-8")
        print(f"\n[OK] Report saved to: {out_path}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
