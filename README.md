# 0.Survey — UAV & Robotics Research Tracker

Systematic 6-tier research survey pipeline for UAV, aerial robotics, multi-agent systems, and related fields.

```
1.Paper          → Single-paper deep dive (reading notes, code experiments)
2.Scholar        → Scholar tracking (Google Scholar profiles, publication history)
3.Lab            → College team real-time tracking (9 labs, arXiv + GitHub)
4.Company        → Industry tracking (Unitree, DJI)
5.UAV Field      → Domain surveys (Anti-UAV, Swarm, UAV+RL, OpenFlight)
6.Tools          → Research productivity tools (Zotero, Obsidian, LaTeX, etc.)
other/           → Miscellaneous & archived items
```

## Quick Start

Open `index.html` in browser for the visual navigation dashboard.

```bash
# Automated research tracking
python track.py --days 14 -o reports/report-$(date +%Y-%m-%d).md
```

## Automated Tracking
- `track.py` — arXiv API + GitHub API weekly report
- Cron job runs every Monday 9:37 AM
- Each lab in `3.Lab/` has its own `dashboard.html` with paper library management
