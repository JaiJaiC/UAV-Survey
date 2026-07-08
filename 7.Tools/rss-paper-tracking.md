# RSS Paper Tracking

`rss_track.py` collects paper candidates from arXiv/RSS feeds into a review inbox:

```bash
python rss_track.py --days 14
```

Default output:

```text
other/inbox/papers_pending.json
```

Design rules:

- Store metadata and links only; do not download PDFs automatically.
- Treat every item as a candidate until manually accepted.
- Keep accepted papers in the existing `papers.json` files or in `1.Paper/` deep-dive folders.
- Put downloaded PDFs outside Git, or use Git LFS only for files that must be versioned.

Useful checks before pushing to GitHub:

```bash
git ls-files | grep -i "\.pdf$"
git count-objects -vH
```

GitHub rejects files larger than 100 MB and warns on files larger than 50 MB. For a survey repository, links plus notes are usually a better default than committing every PDF.
