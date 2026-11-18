# Pollinations API cheat sheet for this skill

Base: https://gen.pollinations.ai  (full reference: APIDOCS.md in pollinations/pollinations)

## Simple GET endpoints (what polli_gen.sh uses)

| Endpoint | Returns | Notes |
| --- | --- | --- |
| GET /text/{prompt} | plain text | `?model=` optional; add `?json=true` or ask for strict JSON in the prompt |
| GET /image/{prompt} | image bytes | `?model= ?width= ?height= ?seed= ?nologo=true`; video models on this same endpoint return MP4 |
| GET /audio/{text} | audio bytes | `?model= ?response_format=mp3 ?duration= ?instrumental=` |

Auth on GET: append `?key=sk_...` (documented browser/script flow) or use a
Bearer header. Anonymous works for many models at lower priority.
`pk_` keys are OAuth client ids for BYOP consent screens, NOT request keys - a
`pk_` sent as a key gets 401.

## Richer endpoints (when GET is not enough)

- POST /v1/chat/completions and /v1/responses - OpenAI-compatible text
- POST /v1/audio/speech - speech/music/SFX with reference_audio conditioning
- POST /v1/images/generations - image generation, JSON response
- GET /v1/models, /image/models, /audio/models, /video/models - catalogues
  with pricing, paid_only flags, durations and per-model capabilities

## Video

Request a video model on the image endpoint, e.g.
`GET /image/{prompt}?model=bytedance/seedance-2.0-fast`.
`?image=<url>` supplies a start frame ([0]) and optional end frame ([1]);
separate multiple URLs with `|`. Check /video/models for video_capabilities
and max_reference_images. Renders can take minutes - poll with a long timeout.

## Billing notes

- Music/video models are usually paid_only; the caller's Pollen balance is
  charged. With no key, request the free tier and expect some models to 402/403.
- paid_only=false does NOT mean zero price: models still meter tiny nonzero
  Pollen per token/second against the caller. Never promise "free"; say
  "free tier" and check /v1/models pricing first.
