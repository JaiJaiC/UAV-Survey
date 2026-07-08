#!/usr/bin/env python3
"""Check tracked repository files for GitHub size risks."""

from __future__ import annotations

import subprocess
from pathlib import Path


WARN_MB = 50
BLOCK_MB = 100
LARGE_EXTS = {".pdf", ".pptx", ".docx", ".doc", ".zip", ".fbx", ".xlsx", ".xls"}


def git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    root = Path(__file__).parent
    tracked = []
    for rel_path in git_ls_files():
        path = root / rel_path
        if not path.exists() or not path.is_file():
            continue
        size_mb = path.stat().st_size / (1024 * 1024)
        if path.suffix.lower() in LARGE_EXTS or size_mb >= WARN_MB:
            tracked.append((size_mb, rel_path))

    tracked.sort(reverse=True)
    total_mb = sum(size for size, _ in tracked)

    print(f"Tracked large/binary-like files: {len(tracked)}")
    print(f"Total shown size: {total_mb:.2f} MB\n")

    risky = False
    for size_mb, rel_path in tracked[:40]:
        marker = "BLOCK" if size_mb >= BLOCK_MB else "WARN" if size_mb >= WARN_MB else "info"
        if size_mb >= WARN_MB:
            risky = True
        print(f"[{marker:5}] {size_mb:8.2f} MB  {rel_path}")

    print("\nGuidance:")
    print("- GitHub blocks individual files over 100 MB.")
    print("- GitHub warns on individual files over 50 MB.")
    print("- Keep paper PDFs local or in Git LFS; commit notes, links, and metadata by default.")
    return 1 if risky else 0


if __name__ == "__main__":
    raise SystemExit(main())
