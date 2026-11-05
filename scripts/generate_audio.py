#!/usr/bin/env python3
"""Generate and track static MP3 audio for Jekyll posts.

The script is deliberately shared by local development and GitHub Actions. It
keeps only audio whose synthesis inputs match the current post, preventing a
stale player from being published after a failed synthesis attempt.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import html
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any
from venv import logger
from xml.sax import handler


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
AUDIO_DIR = ROOT / "assets" / "audio"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"
DATA_PATH = ROOT / "_data" / "audio.json"
GENERATOR_VERSION = 1
DEFAULT_VOICE = "en-US-AndrewNeural"
DEFAULT_RATE = "+0%"
FRONT_MATTER = re.compile(r"\A---\s*\n(?P<data>.*?)\n---\s*\n?(?P<body>.*)\Z", re.DOTALL)


def read_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_post(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text

    metadata: dict[str, str] = {}
    for line in match.group("data").splitlines():
        key, separator, value = line.partition(":")
        if separator and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key.strip()):
            metadata[key.strip()] = value.strip().strip('"\'')
    return metadata, match.group("body")


def spoken_text(markdown: str) -> str:
    """Keep readable prose while preserving paragraph breaks and dropping source-code blocks."""
    # 1. Drop fenced code blocks and inline-code delimiters
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    
    # 2. Drop images and any attached Kramdown/Jekyll attribute blocks like {:style=...}
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)(\{[^}]*\})?", r"\1", text)
    text = re.sub(r"\{:[^}]*\}", " ", text)
    
    # 3. Drop horizontal rules (---, ***, ___ on their own lines)
    text = re.sub(r"^\s{0,3}([-*_]){3,}\s*$", "", text, flags=re.MULTILINE)
    
    # 4. Drop links, comments, and HTML tags
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\[[^]]*\]", r"\1", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    
    # 5. Clean up list markers, blockquotes, and text formatting emphasis
    text = re.sub(r"^\s{0,3}(?:[-+*]|\d+\.)\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{0,3}[>]+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~]", "", text)

    # 6. Target headers, add terminal punctuation if missing, and force a line break for pausing
    def add_header_pause(match):
        heading_text = match.group(1).strip()
        if not heading_text:
            return ""
        if not heading_text.endswith(('.', '!', '?', ':', ';', ',')):
            heading_text += '.'
        return heading_text + "\n"

    text = re.sub(r"^\s{0,3}[#]+\s+(.*)$", add_header_pause, text, flags=re.MULTILINE)
    
    # 7. Clean up internal horizontal whitespace (spaces/tabs) line-by-line, keeping paragraph newlines intact
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    
    return html.unescape(text).strip()


def input_hash(text: str, voice: str, rate: str) -> str:
    payload = json.dumps(
        {"generator_version": GENERATOR_VERSION, "rate": rate, "text": text, "voice": voice},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def audio_filename(relative_path: str) -> str:
    stem = Path(relative_path).stem
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:12]
    return f"{digest}-{stem}.mp3"


async def synthesize(text: str, voice: str, rate: str, destination: Path) -> None:
    import edge_tts

    temporary = destination.with_suffix(".tmp")
    communicator = edge_tts.Communicate(text, voice=voice, rate=rate)
    
    print("   [TTS] Connecting to Microsoft neural engine and generating stream...", flush=True)
    await communicator.save(str(temporary))
    print("   [TTS] Synthesis complete! Saving file...", flush=True)
    
    temporary.replace(destination)


def remove_audio(record: dict[str, Any] | None) -> None:
    if record and isinstance(record.get("file"), str):
        (ROOT / record["file"].lstrip("/")).unlink(missing_ok=True)


def is_audio_enabled(metadata: dict[str, str]) -> bool:
    return metadata.get("audio", "").lower() in {"true", "yes", "1"}


def post_paths(requested_post: str | None) -> list[Path]:
    if requested_post:
        path = (ROOT / requested_post).resolve()
        if POSTS_DIR not in path.parents or not path.is_file():
            raise ValueError(f"Post must be an existing file under {POSTS_DIR.relative_to(ROOT)}/")
        return [path]
    return sorted(path for path in POSTS_DIR.iterdir() if path.suffix in {".md", ".markdown"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--post", help="Generate one post, relative to the repository root")
    parser.add_argument("--force", action="store_true", help="Regenerate opted-in posts even when unchanged")
    arguments = parser.parse_args()

    manifest = read_json(MANIFEST_PATH, {"version": GENERATOR_VERSION, "posts": {}})
    existing: dict[str, dict[str, Any]] = manifest.get("posts", {})
    current = dict(existing)
    selected_paths = post_paths(arguments.post)
    selected_keys: set[str] = set()
    failures: list[str] = []

    for path in selected_paths:
        relative_path = path.relative_to(ROOT).as_posix()
        selected_keys.add(relative_path)
        metadata, body = parse_post(path)
        previous = existing.get(relative_path)

        if not is_audio_enabled(metadata):
            remove_audio(previous)
            current.pop(relative_path, None)
            continue

        text = spoken_text(body)
        voice = metadata.get("audio_voice", DEFAULT_VOICE)
        rate = metadata.get("audio_rate", DEFAULT_RATE)
        fingerprint = input_hash(text, voice, rate)
        filename = audio_filename(relative_path)
        output = AUDIO_DIR / filename
        record = {"file": f"/assets/audio/{filename}", "input_hash": fingerprint, "rate": rate, "voice": voice}

        if not arguments.force and previous == record and output.is_file():
            print(f"Up to date: {relative_path}")
            continue

        if not text:
            print(f"Skipping empty post: {relative_path}", file=sys.stderr)
            remove_audio(previous)
            current.pop(relative_path, None)
            continue

        print(f"Generating: {relative_path} ({voice}, {rate})")
        # --- DEBUG DUMP ---
        Path("debug_payload.txt").write_text(text, encoding="utf-8")
        print(f"   [DEBUG] Saved {len(text)} characters to debug_payload.txt")
        # ------------------
        try:
            AUDIO_DIR.mkdir(parents=True, exist_ok=True)
            asyncio.run(synthesize(text, voice, rate, output))
        except Exception as error:  # Keep publishing text if the remote service is unavailable.
            print(f"Audio generation failed for {relative_path}: {error}", file=sys.stderr)
            output.unlink(missing_ok=True)
            remove_audio(previous)
            current.pop(relative_path, None)
            failures.append(relative_path)
            continue

        if previous and previous.get("file") != record["file"]:
            remove_audio(previous)
        current[relative_path] = record

    if not arguments.post:
        for relative_path, record in existing.items():
            if relative_path not in selected_keys:
                remove_audio(record)
                current.pop(relative_path, None)

    manifest_output = {"version": GENERATOR_VERSION, "posts": current}
    write_json(MANIFEST_PATH, manifest_output)
    write_json(DATA_PATH, {"posts": current})
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
