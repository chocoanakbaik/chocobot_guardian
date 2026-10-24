"""Streaming file hashing helpers."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

ALLOWED_ALGORITHMS = {"sha256", "sha1", "md5"}


def hash_file(path: str | Path, algorithms: Iterable[str] = ("sha256",)) -> dict[str, str]:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(str(file_path))
    requested = tuple(dict.fromkeys(a.lower().replace("-", "") for a in algorithms))
    if not requested or any(a not in ALLOWED_ALGORITHMS for a in requested):
        raise ValueError("Algoritma yang didukung: SHA-256, SHA-1, MD5.")
    hashers = {algorithm: hashlib.new(algorithm) for algorithm in requested}
    with file_path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            for hasher in hashers.values():
                hasher.update(chunk)
    return {algorithm: hasher.hexdigest() for algorithm, hasher in hashers.items()}


__all__ = ["hash_file", "ALLOWED_ALGORITHMS"]
