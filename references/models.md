# Model picks for concept-album (verify against /v1/models before running)

## Text (concept, titles, lore)
Any strong chat model works. Cheap defaults: openai/gpt-5.4-nano or the
current free default. Ask for strict JSON and validate it.

## Image (cover art)
Default model (flux-class) is fine. Use seed for reproducible variants and
1024x1024 for covers.

## Music (tracks)
- elevenlabs/music-v2, elevenlabs/music-v2.5 - duration 3-300s, instrumental=true option, reference_audio conditioning
- google/lyria-3.5 - full songs with vocals; describe structure/length in the prompt; no duration param; MP3
- google/lyria-3-clip-preview - one fixed 30s MP3 clip
- stability-ai/stable-audio-3, stable-audio-3-medium - seconds 1-380, seed, negative_prompt; audio-to-audio via reference_audio with strength 0-1

## Sound effects (intros, interludes, transitions)
mirelo/sfx-2.0, sonilo/sonilo-1.1-sfx, elevenlabs/eleven-text-to-sound-v3

## Video (promo clip)
bytedance/seedance-2.0-fast is a good speed/quality default; google/veo-3.1-fast,
kwaivgi/kling-v3.0-std, alibaba/wan-2.7 are alternatives. Feed the cover as
the start frame for visual continuity.
