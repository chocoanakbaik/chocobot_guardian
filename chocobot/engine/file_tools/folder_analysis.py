"""Bounded, read-only folder inventory utilities."""
from __future__ import annotations

import os
from collections import Counter
from pathlib import Path


def analyze_folder(path: str | Path, max_files: int = 10000) -> dict:
    root = Path(path).expanduser()
    if not root.is_dir():
        raise ValueError("Folder tidak ditemukan atau bukan direktori.")
    if max_files < 1:
        raise ValueError("max_files harus lebih besar dari nol.")
    extensions: Counter[str] = Counter()
    largest: list[dict] = []
    total_bytes = 0
    files_seen = directories_seen = inaccessible = 0
    truncated = False
    for current, dir_names, file_names in os.walk(root, followlinks=False):
        base = Path(current)
        dir_names[:] = [d for d in dir_names if not (base / d).is_symlink()]
        directories_seen += len(dir_names)
        for name in file_names:
            file_path = base / name
            if file_path.is_symlink():
                continue
            try:
                if not file_path.is_file():
                    continue
                stat = file_path.stat()
            except OSError:
                inaccessible += 1
                continue
            files_seen += 1
            if files_seen > max_files:
                truncated = True
                break
            total_bytes += stat.st_size
            extensions[file_path.suffix.lower() or "[tanpa ekstensi]"] += 1
            largest.append({"name": str(file_path.relative_to(root)), "size_bytes": stat.st_size})
            largest.sort(key=lambda row: row["size_bytes"], reverse=True)
            del largest[10:]
        if truncated:
            break
    return {
        "root": str(root.resolve()), "files_count": min(files_seen, max_files),
        "directories_count": directories_seen, "total_bytes": total_bytes,
        "extension_counts": dict(extensions.most_common()), "largest_files": largest,
        "inaccessible_count": inaccessible, "truncated": truncated, "max_files": max_files,
    }


__all__ = ["analyze_folder"]
