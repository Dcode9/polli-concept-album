#!/usr/bin/env bash
# polli_gen.sh - one-call generation against the Pollinations GET endpoints.
#
# Usage:
#   polli_gen.sh text   PROMPT OUT.txt [--model M]
#   polli_gen.sh image  PROMPT OUT.jpg [--model M] [--width W] [--height H] [--seed S]
#   polli_gen.sh audio  PROMPT OUT.mp3 [--model M] [--duration N] [--instrumental true]
#   polli_gen.sh video  PROMPT OUT.mp4 [--model M] [--image START_FRAME_URL_OR_PATH]
#
# Auth: reads POLLINATIONS_API_KEY (sk_...) if set and appends it as ?key=.
# The polli CLI (npx @pollinations/cli) can sign the agent in without handling keys.
set -euo pipefail

BASE="https://gen.pollinations.ai"
KIND="${1:?kind: text|image|audio|video}"
PROMPT="${2:?prompt}"
OUT="${3:?outfile}"
shift 3

MODEL="" ; WIDTH="" ; HEIGHT="" ; SEED="" ; DURATION="" ; INSTRUMENTAL="" ; IMAGE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --model) MODEL="$2"; shift 2;;
    --width) WIDTH="$2"; shift 2;;
    --height) HEIGHT="$2"; shift 2;;
    --seed) SEED="$2"; shift 2;;
    --duration) DURATION="$2"; shift 2;;
    --instrumental) INSTRUMENTAL="$2"; shift 2;;
    --image) IMAGE="$2"; shift 2;;
    *) echo "unknown flag: $1" >&2; exit 2;;
  esac
done

enc() { python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }
EP="$PROMPT"
case "$KIND" in
  text)  URL="$BASE/text/$(enc "$EP")";;
  image) URL="$BASE/image/$(enc "$EP")?nologo=true";;
  audio) URL="$BASE/audio/$(enc "$EP")?response_format=mp3";;
  video) URL="$BASE/image/$(enc "$EP")"; [ -n "$MODEL" ] || MODEL="bytedance/seedance-2.0-fast";;
  *) echo "bad kind" >&2; exit 2;;
esac

sep() { case "$1" in *\?*) echo '&';; *) echo '?';; esac; }
add() { URL="$URL$(sep "$URL")$1"; }

[ -n "$MODEL" ]        && add "model=$(enc "$MODEL")"
[ -n "$WIDTH" ]        && add "width=$WIDTH"
[ -n "$HEIGHT" ]       && add "height=$HEIGHT"
[ -n "$SEED" ]         && add "seed=$SEED"
[ -n "$DURATION" ]     && add "duration=$DURATION"
[ -n "$INSTRUMENTAL" ] && add "instrumental=$INSTRUMENTAL"
[ -n "$IMAGE" ]        && add "image=$(enc "$IMAGE")"
if [ -n "${POLLINATIONS_API_KEY:-}" ]; then add "key=$POLLINATIONS_API_KEY"; fi

# Video renders are slow: allow 10 minutes, everything else 3.
if [ "$KIND" = "video" ]; then MAX=600; else MAX=180; fi
echo "GET ${URL%%\?*} (params hidden)" >&2
curl -fsSL --max-time "$MAX" -o "$OUT" "$URL" || { echo "generation failed for $OUT" >&2; exit 1; }

# Sanity: reject tiny or HTML error bodies saved as media.
SZ=$(wc -c < "$OUT")
if [ "$KIND" != "text" ]; then
  if [ "$SZ" -lt 2000 ]; then echo "suspiciously small output ($SZ bytes): $OUT" >&2; exit 1; fi
  HEAD=$(head -c 16 "$OUT" | tr -d '\0')
  case "$HEAD" in *'<!'*|*'<html'*|*'{\"error'*) echo "output looks like an error page: $OUT" >&2; exit 1;; esac
fi
echo "wrote $OUT ($SZ bytes)" >&2
