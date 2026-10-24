"""Tests for the limited read-only file heuristic analyzer."""
import hashlib
from pathlib import Path

from chocobot.engine.security.file_analyzer import analyze_file


def test_double_extension_is_flagged_without_claiming_malware(tmp_path: Path):
    target = tmp_path / "invoice.pdf.exe"
    target.write_bytes(b"MZsample")
    result = analyze_file(target)

    codes = {item["code"] for item in result["notes"]}
    assert "executable-or-script" in codes
    assert "double-extension" in codes
    assert result["sha256"] == hashlib.sha256(b"MZsample").hexdigest()
    assert "not an antivirus" in result["notice"] or "bukan antivirus" in result["notice"]


def test_extension_signature_mismatch_is_reported(tmp_path: Path):
    target = tmp_path / "notes.pdf"
    target.write_text("plain text instead of PDF", encoding="utf-8")
    result = analyze_file(target)
    assert "signature-mismatch" in {item["code"] for item in result["notes"]}


def test_clean_text_file_is_reported_as_no_simple_indicator(tmp_path: Path):
    target = tmp_path / "notes.txt"
    target.write_text("ordinary notes", encoding="utf-8")
    result = analyze_file(target)
    assert result["notes"] == []
    assert result["overall_attention"] == "Tidak ada indikator pada aturan sederhana"
