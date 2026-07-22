# 2. Scholar Tracking

Tracking individual researchers: their publication history, research directions, and academic impact.

## Canonical layout

All browsable directory pages use `index.html`. Paper assets live directly below each scholar's `files` directory:

```text
2.Scholar/
├── index.html
└── <Scholar>/
    ├── index.html
    ├── <Scholar>.rdf
    └── files/
        ├── index.html
        └── <paper-id>/
            ├── index.html     # redirects to note.html
            ├── note.html      # required third-level paper notes
            ├── figures/       # source-grounded figures/page snapshots
            └── <paper assets>
```

Each scholar `index.html` remains the second-level navigation dashboard and links directly to each paper's third-level `note.html`. The note structure follows `1.Paper/0.Fracture/note.html` (`Info`, `Insight`, `Architecture`, `Task`, `Challenge`, `Method`, `Principles`, `Figures`, `Flaw`, and `Motivation`).

Run `python tools/rebuild_scholar_indexes.py` after adding or reorganizing papers. It flattens legacy duplicate scholar folders, preserves the original scholar dashboards, supplements new navigation cards, rebuilds directory redirects, and refreshes the scholar cards on the site home page.

## Resources
- `google scholar.txt` — collection of Google Scholar profile links

## Methodology
- Google Scholar alerts for new papers
- arXiv author search
- Personal/lab website monitoring
