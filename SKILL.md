---
name: concept-album
description: Turn any theme, mood, place, or story into a complete fictional album drop with Pollinations models - invented band, track list, cover art, real generated music tracks, an optional promo video clip, and a static player page. Use when the user wants a creative audio-visual artifact, an album or EP concept, a soundtrack, a mixtape, or a musical gift.
---

# Concept Album

Build a whole fictional album from one theme. The agent invents the band and
music with a text model, generates the cover with an image model, renders real
audio with Pollinations music models, optionally cuts a promo clip with a video
model, then assembles and verifies a static player page.

Everything runs through `scripts/polli_gen.sh`, a thin wrapper over the
Pollinations GET endpoints. No SDK install is required.

## Auth

- Easiest: the `polli` CLI (`npx @pollinations/cli`) signs agents in without
  handling keys; once signed in, requests work with its managed key.
- Or set `POLLINATIONS_API_KEY` to an `sk_...` key (from enter.pollinations.ai).
  `polli_gen.sh` reads it and appends `?key=` / `&key=` for you.
- Never print, log, or commit a key. Keys in URLs are for local scripts only.
- Free anonymous requests work for many models at lower priority; check
  https://gen.pollinations.ai/v1/models for `paid_only` flags before choosing
  a model. If the user wants a paid model, they pay with their own Pollen -
  confirm the spend first (see BRING_YOUR_OWN_POLLEN.md in the Pollinations
  repo).

## Workflow

### 1. Concept (text model)

Pick a theme with the user (or infer one). Ask a text model for the album
concept as strict JSON, then save it as `album.json`:

```
{
  "band": "string",
  "album": "string",
  "tagline": "string",
  "genre": "string",
  "cover_prompt": "detailed image prompt, no text overlay instructions",
  "tracks": [
    {"title": "string", "mood": "string", "prompt": "music prompt",
     "seconds": 60, "instrumental": true}
  ],
  "promo_prompt": "optional 4-8s video prompt"
}
```

Example:
`./scripts/polli_gen.sh text 'Return ONLY JSON for a fictional album about monsoon nights in Mumbai...' concept.json`
Then validate the JSON (`python3 -m json.tool`) and keep 3-6 tracks.

### 2. Cover art (image model)

`./scripts/polli_gen.sh image "$(jq -r .cover_prompt album.json)" cover.jpg --width 1024 --height 1024`

### 3. Tracks (music models)

One file per track, MP3:

`./scripts/polli_gen.sh audio "dreamy synthwave ballad, slow, 80s arpeggios" track-01.mp3 --model elevenlabs/music-v2.5 --duration 60 --instrumental true`

Model notes (check /v1/models for current availability and pricing):
- `elevenlabs/music-v2`, `elevenlabs/music-v2.5`: 3-300s, `instrumental=true` option
- `google/lyria-3.5`: full songs, describe structure and length in the prompt, no duration param
- `google/lyria-3-clip-preview`: fixed 30s clip
- `stability-ai/stable-audio-3*`: `seconds` 1-380, supports seed and negative_prompt
- Sound effects for intros/interludes: `mirelo/sfx-2.0`, `sonilo/sonilo-1.1-sfx`, `elevenlabs/eleven-text-to-sound-v3`

### 4. Promo clip (video model, optional)

`./scripts/polli_gen.sh video "$(jq -r .promo_prompt album.json)" promo.mp4 --model bytedance/seedance-2.0-fast --image cover.jpg`

Passing the cover as the start frame ties the clip to the art.

### 5. Player page

`python3 scripts/build_player.py album.json -o site/`
Writes a self-contained `site/index.html` with the cover, track list, and
HTML5 audio players, plus a copy of the assets.

### 6. Verify (required before delivery)

`python3 scripts/verify_album.py album.json site/`
Fails unless every track in the manifest exists on disk, decodes as the right
media type, is non-trivial in size, and every file the player references is
present. Never deliver an album that skips verification; fix or regenerate the
failing asset and re-run.

## Taste guidance

- Commit to a bit: a fake band is better with a name, a lore one-liner, and
  track titles that could not belong to any other album.
- Instrumental tracks read as "more real" for lo-fi/soundtrack concepts;
  lyric songs shine for parody or anthem concepts (lyria-3.5).
- Keep the cover prompt free of words-in-image requests unless the model is
  known to render text well; put typography in the player page instead.
