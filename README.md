# concept-album

An [Agent Skills](https://agentskills.io) skill: your coding agent turns any
theme into a complete fictional album drop with
[Pollinations](https://pollinations.ai) models - invented band, track list,
cover art, real generated music, an optional promo clip, and a static player
page, all verified before delivery.

[![Made with pollinations.ai](https://raw.githubusercontent.com/pollinations/pollinations/main/packages/ui/src/brand/badge-made-with.svg)](https://pollinations.ai/?ref=badge)

## What the agent does

1. Invents the band, lore, and track list with a text model (JSON manifest)
2. Renders the cover with an image model
3. Generates each track with a music model (elevenlabs/music-v2.5, google/lyria-3.5, stable-audio-3, ...)
4. Optional: cuts a promo clip with a video model, using the cover as the start frame
5. Assembles a self-contained player page (`scripts/build_player.py`)
6. Verifies every asset against the manifest (`scripts/verify_album.py`) - no unverified album ships

## Use

Copy `SKILL.md`, `scripts/` and `references/` into your agent's skills
directory, or point your agent at this repo. Then ask for an album:

> Make me a concept album about night trains across the Deccan.

Auth is handled by the [polli CLI](https://www.npmjs.com/package/@pollinations/cli)
(signs agents in without handling keys) or a `POLLINATIONS_API_KEY` env var.
Users pay with their own Pollen when they pick paid models - see
[Pollinations Pay](https://github.com/pollinations/pollinations/blob/main/BRING_YOUR_OWN_POLLEN.md).

## Layout

- `SKILL.md` - the skill (Agent Skills format)
- `scripts/polli_gen.sh` - one-call generation against the Pollinations GET endpoints
- `scripts/build_player.py` - manifest -> static player page
- `scripts/verify_album.py` - pre-delivery verification gate
- `references/` - endpoint and model cheat sheets
- `examples/` - a finished album drop
