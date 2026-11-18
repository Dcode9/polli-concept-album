#!/usr/bin/env python3
"""Assemble a static player page for a concept album.

Usage: build_player.py album.json -o site/

Copies cover/tracks/promo into the output dir and writes index.html:
cover, band lore, track list with HTML5 audio players, optional promo video.
"""
import argparse, html, json, os, shutil, sys

TEMPLATE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{album} - {band}</title>
<style>
  body {{ background:#0d0d12; color:#e8e6f0; font-family:Georgia,serif;
         max-width:680px; margin:0 auto; padding:32px 16px; }}
  img.cover {{ width:100%; border-radius:12px; }}
  h1 {{ margin:16px 0 0; font-size:2rem; }}
  h2 {{ margin:0; font-weight:normal; color:#9a94b8; font-size:1.1rem; }}
  p.tag {{ color:#6f6a8c; font-style:italic; }}
  ol.tracks {{ list-style:none; padding:0; }}
  ol.tracks li {{ margin:18px 0; padding:14px; background:#16161f; border-radius:10px; }}
  ol.tracks .t {{ display:flex; justify-content:space-between; margin-bottom:8px; }}
  ol.tracks .mood {{ color:#6f6a8c; font-size:.85rem; }}
  audio {{ width:100%; }}
  video {{ width:100%; border-radius:12px; margin-top:24px; }}
  footer {{ margin-top:32px; color:#555; font-size:.8rem; }}
</style></head><body>
<img class="cover" src="{cover}" alt="Cover art for {album}">
<h1>{album}</h1>
<h2>{band} - {genre}</h2>
<p class="tag">{tagline}</p>
<ol class="tracks">
{tracks}
</ol>
{promo}
<footer>Made with <a href="https://pollinations.ai/?ref=badge">Pollinations</a> models by an agent running the concept-album skill.</footer>
</body></html>
"""

TRACK = """  <li><div class="t"><span>{n}. {title}</span><span class="mood">{mood}</span></div>
  <audio controls preload="none" src="{file}"></audio></li>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    base = os.path.dirname(os.path.abspath(a.manifest))
    m = json.load(open(a.manifest))
    os.makedirs(a.out, exist_ok=True)

    def copy(fn):
        src = os.path.join(base, fn)
        if not os.path.exists(src):
            sys.exit(f"missing asset: {fn}")
        shutil.copy2(src, os.path.join(a.out, fn))
        return fn

    cover = copy(m.get("cover") or "cover.jpg")
    lis = []
    for i, t in enumerate(m["tracks"], 1):
        fn = copy(t.get("file") or f"track-{i:02d}.mp3")
        lis.append(TRACK.format(n=i, title=html.escape(t["title"]),
                                mood=html.escape(t.get("mood", "")), file=html.escape(fn)))
    promo_html = ""
    if m.get("promo"):
        pf = copy(m["promo"])
        promo_html = f'<video controls loop muted playsinline src="{html.escape(pf)}"></video>'

    page = TEMPLATE.format(
        album=html.escape(m["album"]), band=html.escape(m["band"]),
        genre=html.escape(m.get("genre", "")), tagline=html.escape(m.get("tagline", "")),
        cover=html.escape(cover), tracks="\n".join(lis), promo=promo_html)
    with open(os.path.join(a.out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {a.out}/index.html with {len(lis)} tracks")

if __name__ == "__main__":
    main()
