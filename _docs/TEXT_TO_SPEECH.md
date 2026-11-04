# Text-to-speech posts

Posts opt in to generated audio with front matter:

```yaml
audio: true
```

The generated MP3 uses `en-US-AndrewNeural` by default. Override the voice or rate for an individual post when needed:

```yaml
audio: true
audio_voice: en-US-AndrewNeural
audio_rate: "+0%"
```

## Generate audio locally

The commands use [uv](https://docs.astral.sh/uv/), which automatically downloads the pinned Python version and generator dependencies on first use. To prepare them ahead of time, run:

```sh
make audio-install
```

Then generate missing or outdated audio for all opted-in posts:

```sh
make audio
```

To generate one post only:

```sh
make audio POST=_posts/2026-11-04-genai-basic-notions.md
```

To force regeneration of every opted-in post, for example after changing the default voice:

```sh
make audio-all
```

The generator records a SHA-256 hash of the normalized spoken text, voice, rate, and generator version in `assets/audio/manifest.json`. It reuses an MP3 when that input hash is unchanged and regenerates only posts with a changed or missing hash.

The GitHub Actions workflow uses this same `uv run` command and the locked dependencies. It generates audio before building and deploying the site. If synthesis fails for a post, the generated data file omits that post, so its text is deployed without an audio player or a stale MP3.

Audio is generated through the community-maintained `edge-tts` package, which accesses Microsoft Edge's online speech service without an API key. It does not require Edge to be installed on the generator or reader's device.
