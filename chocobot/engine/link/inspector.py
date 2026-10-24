"""Local, offline URL inspection using explainable heuristic indicators."""
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlsplit, unquote

SHORTENER_HOSTS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "buff.ly", "cutt.ly", "rb.gy", "shorturl.at"}
SUSPICIOUS_TLDS = {"zip", "mov", "click", "top", "work", "country", "gq", "tk", "ml", "cf"}
SAFE_SCHEMES = {"http", "https"}


def inspect_url(value: str) -> dict:
    """Inspect URL structure without contacting the host; result is not a malware verdict."""
    raw = value.strip() if isinstance(value, str) else ""
    if not raw:
        return {"valid": False, "error": "Masukkan URL terlebih dahulu.", "score": 0, "level": "Tidak dinilai", "indicators": []}
    candidate = raw if "://" in raw else "https://" + raw
    try:
        parsed = urlsplit(candidate)
        scheme = parsed.scheme.lower()
        hostname = (parsed.hostname or "").rstrip(".").lower()
        port = parsed.port
    except ValueError:
        return {"valid": False, "error": "Format URL atau nomor port tidak valid.", "score": 0, "level": "Tidak dinilai", "indicators": []}
    if scheme not in SAFE_SCHEMES or not hostname:
        return {"valid": False, "error": "URL harus menggunakan http:// atau https:// dan memiliki host.", "score": 0, "level": "Tidak dinilai", "indicators": []}

    indicators: list[dict] = []
    points = 0

    def add(code: str, title: str, detail: str, weight: int) -> None:
        nonlocal points
        indicators.append({"code": code, "title": title, "detail": detail, "points": weight})
        points += weight

    try:
        ipaddress.ip_address(hostname.strip("[]"))
        add("ip-host", "Host berupa alamat IP", "URL menggunakan alamat IP alih-alih nama domain.", 18)
    except ValueError:
        pass
    if parsed.username is not None or parsed.password is not None or "@" in parsed.netloc:
        add("userinfo", "Informasi login ada di bagian host", "Tanda @ atau kredensial pada URL dapat menyamarkan tujuan tautan.", 30)
    labels = hostname.split(".")
    if any(label.startswith("xn--") for label in labels):
        add("punycode", "Domain menggunakan Punycode", "Periksa karakter domain untuk memastikan tidak meniru nama lain.", 22)
    if hostname in SHORTENER_HOSTS:
        add("shortener", "Layanan pemendek URL", "Tujuan akhir belum terlihat dari URL singkat ini.", 12)
    tld = labels[-1] if labels else ""
    if tld in SUSPICIOUS_TLDS:
        add("tld-review", "Akhiran domain perlu ditinjau", f"Akhiran .{tld} kadang digunakan dalam tautan berisiko, tetapi bukan bukti bahaya.", 8)
    if len(labels) >= 5:
        add("many-subdomains", "Banyak subdomain", "Periksa domain registrable yang sebenarnya; nama di sebelah kiri dapat mengelabui pembaca.", 10)
    if port is not None and port not in (80, 443):
        add("nonstandard-port", "Port nonstandar", f"URL menggunakan port {port}. Pastikan layanan dan tujuan port memang diharapkan.", 10)
    if scheme != "https":
        add("no-https", "Tidak menggunakan HTTPS", "Koneksi HTTP tidak mengenkripsi lalu lintas ke server tujuan.", 12)
    if len(raw) > 180:
        add("long-url", "URL sangat panjang", "URL panjang dapat menyulitkan pemeriksaan tujuan dan parameter.", 5)
    decoded = unquote(parsed.path + "?" + parsed.query)
    if re.search(r"%(?:2f|5c|40|3a)", parsed.path + parsed.query, re.IGNORECASE):
        add("encoded-delimiters", "Karakter pembatas di-encode", "Periksa path dan parameter setelah decoding untuk memahami tujuan sebenarnya.", 8)
    if re.search(r"(?:login|verify|password|wallet|payment|account|secure|update)[-_.\/]", decoded, re.IGNORECASE):
        add("credential-words", "Path berisi kata terkait akun atau login", "Kata-kata ini juga umum pada layanan sah; cocokkan domain dan konteks sebelum membuka.", 8)

    score = min(points, 100)
    level = "Rendah" if score < 20 else "Sedang" if score < 45 else "Tinggi" if score < 70 else "Sangat tinggi"
    return {
        "valid": True, "original": raw, "normalized_url": candidate,
        "scheme": scheme, "host": hostname,
        "port": port or (443 if scheme == "https" else 80),
        "path": parsed.path or "/", "query_present": bool(parsed.query),
        "fragment_present": bool(parsed.fragment), "https": scheme == "https",
        "score": score, "level": level, "indicators": indicators,
        "notice": "Skor adalah indikator heuristik lokal, bukan hasil pemindaian internet dan bukan bukti bahwa tautan aman atau berbahaya.",
    }


__all__ = ["inspect_url"]
