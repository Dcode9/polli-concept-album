#!/usr/bin/env python3
"""Verify an album directory against its manifest before delivery.

Usage: verify_album.py album.json [site_dir]

Checks:
  - manifest parses and has band, album, and >=1 track
  - every track file named in the manifest exists, is >10 KB, and sniffs as MP3
  - the cover exists and sniffs as JPEG/PNG/WebP
  - optional promo.mp4 sniffs as MP4 (ftyp box)
  - if site_dir is given, index.html exists and every src/href it references
    resolves to a file inside site_dir
Exits non-zero and prints every failure found.
"""
import json, os, re, sys

def sniff(path):
    try:
        with open(path, "rb") as f:
            return f.read(16)
    except OSError:
        return b""

def is_mp3(h): return h[:3] == b"ID3" or h[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")
def is_img(h): return h[:3] == b"\xff\xd8\xff" or h[:8] == b"\x89PNG\r\n\x1a\n" or (h[:4] == b"RIFF" and h[8:12] == b"WEBP")
def is_mp4(h): return h[4:8] == b"ftyp"

def main():
    failures = []
    if len(sys.argv) < 2:
        print("usage: verify_album.py album.json [site_dir]"); return 2
    mpath = sys.argv[1]
    base = os.path.dirname(os.path.abspath(mpath))
    try:
        m = json.load(open(mpath))
    except Exception as e:
        print(f"FAIL: manifest does not parse: {e}"); return 1
    for field in ("band", "album"):
        if not m.get(field): failures.append(f"manifest missing '{field}'")
    tracks = m.get("tracks") or []
    if not tracks: failures.append("manifest has no tracks")

    for i, t in enumerate(tracks, 1):
        fn = t.get("file") or f"track-{i:02d}.mp3"
        p = os.path.join(base, fn)
        if not os.path.exists(p):
            failures.append(f"track {i} missing: {fn}"); continue
        if os.path.getsize(p) < 10_000:
            failures.append(f"track {i} too small (<10 KB): {fn}")
        if not is_mp3(sniff(p)):
            failures.append(f"track {i} is not MP3 data: {fn}")
        if not t.get("title"):
            failures.append(f"track {i} has no title")

    cover = m.get("cover") or "cover.jpg"
    cp = os.path.join(base, cover)
    if not os.path.exists(cp): failures.append(f"cover missing: {cover}")
    elif not is_img(sniff(cp)): failures.append(f"cover is not JPEG/PNG/WebP: {cover}")

    promo = m.get("promo")
    if promo:
        pp = os.path.join(base, promo)
        if not os.path.exists(pp): failures.append(f"promo missing: {promo}")
        elif not is_mp4(sniff(pp)): failures.append(f"promo is not MP4: {promo}")

    if len(sys.argv) > 2:
        site = sys.argv[2]
        idx = os.path.join(site, "index.html")
        if not os.path.exists(idx):
            failures.append("site index.html missing")
        else:
            html = open(idx, encoding="utf-8", errors="replace").read()
            for ref in set(re.findall(r'(?:src|href)="([^"#]+)"', html)):
                if ref.startswith(("http://", "https://", "data:")): continue
                if not os.path.exists(os.path.join(site, ref)):
                    failures.append(f"player references missing file: {ref}")

    if failures:
        print("ALBUM NOT READY:")
        for f in failures: print(f"  FAIL: {f}")
        return 1
    print(f"OK: {m.get('band')} - {m.get('album')} ({len(tracks)} tracks) verified")
    return 0

if __name__ == "__main__":
    sys.exit(main())
