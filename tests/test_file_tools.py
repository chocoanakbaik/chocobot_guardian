"""Tests for read-only file metadata, hashing and folder inventory."""
import hashlib
from pathlib import Path

import pytest

from chocobot.engine.file_tools.file_info import get_file_info
from chocobot.engine.file_tools.folder_analysis import analyze_folder
from chocobot.engine.file_tools.hashing import hash_file


def test_file_metadata_and_sha256_are_consistent(tmp_path: Path):
    target = tmp_path / "hello.txt"
    target.write_text("chocobot local test", encoding="utf-8")

    info = get_file_info(target)
    digest = hash_file(target, ("sha256",))["sha256"]

    assert info["name"] == "hello.txt"
    assert info["extension"] == ".txt"
    assert info["size_bytes"] == len("chocobot local test".encode("utf-8"))
    assert digest == hashlib.sha256(b"chocobot local test").hexdigest()


def test_hashing_rejects_missing_file_and_unknown_algorithm(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        hash_file(tmp_path / "missing.dat")
    target = tmp_path / "sample.dat"
    target.write_bytes(b"abc")
    with pytest.raises(ValueError):
        hash_file(target, ("sha999",))


def test_folder_analysis_counts_files_and_tracks_largest(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.bin").write_bytes(b"123456")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.txt").write_text("xyz", encoding="utf-8")

    result = analyze_folder(tmp_path)

    assert result["files_count"] == 3
    assert result["total_bytes"] == 10
    assert result["extension_counts"][".txt"] == 2
    assert result["largest_files"][0]["name"] == "b.bin"
    assert result["truncated"] is False


def test_folder_analysis_has_a_safe_file_count_limit(tmp_path: Path):
    for name in ("a.txt", "b.txt", "c.txt"):
        (tmp_path / name).write_text(name, encoding="utf-8")
    result = analyze_folder(tmp_path, max_files=1)
    assert result["files_count"] == 1
    assert result["truncated"] is True
