"""Read-only heuristic inspection of one file; not an antivirus engine."""
from __future__ import annotations

import hashlib
from pathlib import Path

from chocobot.engine.file_tools.file_info import get_file_info

RISKY_EXECUTABLES = {".exe", ".dll", ".scr", ".com", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jse", ".wsf", ".hta", ".msi", ".reg", ".lnk"}
MACRO_FORMATS = {".docm", ".xlsm", ".pptm", ".dotm", ".xlam"}
DOUBLE_EXTENSION_MARKERS = RISKY_EXECUTABLES | MACRO_FORMATS | {".pdf", ".docx", ".xlsx", ".jpg", ".png"}


def analyze_file(path: str | Path, include_sha256: bool = True) -> dict:
    target = Path(path).expanduser()
    info = get_file_info(target)
    notes: list[dict] = []
    name_parts = [part.lower() for part in target.name.split(".") if part]
    extension = target.suffix.lower()
    executable_suffixes = {item.lstrip(".") for item in RISKY_EXECUTABLES}
    marker_suffixes = {item.lstrip(".") for item in DOUBLE_EXTENSION_MARKERS}
    if extension in RISKY_EXECUTABLES:
        notes.append({"attention": "Tinggi", "code": "executable-or-script", "detail": "File dapat menjalankan kode atau perintah. Buka hanya jika sumber dan tujuan file sudah dipercaya."})
    if extension in MACRO_FORMATS:
        notes.append({"attention": "Tinggi", "code": "macro-document", "detail": "Format dokumen ini dapat berisi macro. Jangan aktifkan macro dari sumber tak dikenal."})
    if len(name_parts) >= 3 and name_parts[-1] in executable_suffixes and name_parts[-2] in marker_suffixes:
        notes.append({"attention": "Tinggi", "code": "double-extension", "detail": "Nama file memiliki ekstensi ganda yang dapat menyamarkan tipe file akhir."})
    signatures = {
        ".pdf": b"%PDF-", ".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff",
        ".jpeg": b"\xff\xd8\xff", ".gif": b"GIF8", ".zip": b"PK\x03\x04",
    }
    expected = signatures.get(extension)
    if expected:
        try:
            with target.open("rb") as stream:
                header = stream.read(max(8, len(expected)))
            if not header.startswith(expected):
                notes.append({"attention": "Sedang", "code": "signature-mismatch", "detail": "Isi awal file tidak cocok dengan signature umum untuk ekstensi ini. File mungkin rusak atau memakai ekstensi yang menyesatkan."})
        except OSError:
            pass
    if info["size_bytes"] > 100 * 1024 * 1024:
        notes.append({"attention": "Informasi", "code": "large-file", "detail": "File lebih besar dari 100 MB; proses lebih lanjut dapat membutuhkan waktu dan sumber daya lebih banyak."})
    digest = None
    if include_sha256:
        hasher = hashlib.sha256()
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
        digest = hasher.hexdigest()
    return {
        "file": info, "sha256": digest, "notes": notes,
        "overall_attention": "Tinggi" if any(n["attention"] == "Tinggi" for n in notes) else "Perlu ditinjau" if notes else "Tidak ada indikator pada aturan sederhana",
        "notice": "Pemeriksaan berbasis metadata dan signature terbatas. Ini bukan antivirus, tidak membuktikan file aman, dan tidak mengirim file ke layanan online.",
    }


__all__ = ["analyze_file"]
