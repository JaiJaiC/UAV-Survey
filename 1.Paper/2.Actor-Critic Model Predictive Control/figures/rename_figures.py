#!/usr/bin/env python3
"""
rename_figures.py — 按文件修改时间顺序重命名 figures/ 下的图片

用法:
    python rename_figures.py                # 处理当前目录下的 figures/
    python rename_figures.py /path/to/paper # 处理指定目录下的 figures/

规则:
    - 时间最早的图片 → fig1.<ext>, 次早 → fig2.<ext>, ...
    - 保留原始扩展名（png→png, jpg→jpg, ...）
    - 以文件「修改时间」(mtime) 排序
    - 仅处理常见图片格式: png, jpg, jpeg, gif, bmp, webp, tiff, svg
"""

import os
import sys
from pathlib import Path

IMG_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.svg'}


def rename_figures(paper_dir: str | None = None) -> None:
    # 确定 figures 目录
    base = Path(paper_dir) if paper_dir else Path.cwd()
    fig_dir = base / 'figures'
    if not fig_dir.is_dir():
        fig_dir = base  # 如果 figures/ 不存在，直接用 base 本身
    if not fig_dir.is_dir():
        print(f"[ERROR] 目录不存在: {fig_dir}")
        sys.exit(1)

    # 收集所有图片文件
    images: list[Path] = []
    for f in fig_dir.iterdir():
        if f.is_file() and f.suffix.lower() in IMG_EXTS:
            images.append(f)

    if not images:
        print("[INFO] figures/ 下没有找到图片文件，无需操作。")
        return

    # 按修改时间排序（最早的排前面）
    images.sort(key=lambda f: f.stat().st_mtime)

    print(f"[INFO] 找到 {len(images)} 张图片，按修改时间排序:") # 中文提示
    for i, f in enumerate(images, 1):
        import datetime
        mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime)
        print(f"  {i:2d}. {f.name:40s}  {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

    # 先全部重命名为临时名字，避免命名冲突
    tmp_names: list[Path] = []
    for i, f in enumerate(images):
        tmp = fig_dir / f'_tmp_rename_{i:04d}{f.suffix}'
        f.rename(tmp)
        tmp_names.append(tmp)

    # 再按目标名字重命名
    for i, tmp in enumerate(tmp_names, 1):
        target = fig_dir / f'fig{i}{tmp.suffix}'
        if target.exists():
            # 如果目标已存在（比如手动命名的 fig1.png），先删掉
            target.unlink()
        tmp.rename(target)

    print(f"\n[OK] 重命名完成 — images renamed successfully:") # 中文提示
    for i in range(1, len(images) + 1):
        for f in fig_dir.iterdir():
            if f.stem == f'fig{i}':
                print(f"  {f.name}")
                break


if __name__ == '__main__':
    paper_dir = sys.argv[1] if len(sys.argv) > 1 else None
    rename_figures(paper_dir)
