# Examples

`midnight-local/` holds a sample `album.json` manifest and the player page
`build_player.py` builds from it, so you can see the exact shape of the
skill's output without running anything.

**No generated binaries are committed.** Rendering cover art and tracks calls
Pollinations models that charge the caller's Pollen, and this repository is
maintained under a no-spend constraint. When you run the skill, your agent
renders the assets with your own key (BYOP) and drops them next to the
manifest; `verify_album.py` then checks them before delivery.

The committed audio/cover files, when present in a run's working directory,
are what `verify_album.py` validates: real MP3/JPEG/PNG data, non-trivial
size, every manifest entry present, every player reference resolvable. The
assembly and verification pipeline itself is smoke-tested end to end with
clearly-labeled synthetic stand-ins - that tests the plumbing, not the
models, and we say so rather than pass off tones as generated music.
