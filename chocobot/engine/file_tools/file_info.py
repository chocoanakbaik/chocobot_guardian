"""Metadata-only file information helpers."""
from __future__ import annotations

import mimetypes
from pathlib import Path


def get_file_info(path: str | Path) -> dict:
    file_path = Path(path).expanduser()
    stat = file_path.stat()
    if not file_path.is_file():
        raise ValueError("Jalur yang dipilih bukan file biasa.")
    mime, _ = mimetypes.guess_type(file_path.name)
    return {
        "name": file_path.name, "full_path": str(file_path.resolve()),
        "extension": file_path.suffix.lower(), "mime_type": mime or "Tidak diketahui",
        "size_bytes": stat.st_size, "modified_time": stat.st_mtime,
        "created_time": stat.st_ctime,
        "is_hidden": file_path.name.startswith(".") or file_path.name.startswith("~"),
        "is_symlink": file_path.is_symlink(),
    }


__all__ = ["get_file_info"]
