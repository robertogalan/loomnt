"""Loom helpers: extract the video ID, fetch the transcript, download the MP4."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import requests

_VIDEO_ID_RE = re.compile(r"([0-9a-fA-F]{32})")
_GRAPHQL_URL = "https://www.loom.com/graphql"
_TIMESTAMP_TAG_RE = re.compile(r"<[^>]+>")


def extract_video_id(url: str) -> str:
    """Extract the 32-char hex video ID from a Loom share/embed URL."""
    match = _VIDEO_ID_RE.search(url)
    if not match:
        raise ValueError(
            f"Could not find a Loom video ID in URL: {url!r}. "
            "Expected a loom.com/share/<id> or loom.com/embed/<id> link."
        )
    return match.group(1).lower()


def _seconds_to_mmss(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def _parse_vtt(vtt: str) -> str:
    """Turn a WebVTT captions blob into 'MM:SS  text' lines."""
    lines: list[str] = []
    current_ts: str | None = None
    for raw in vtt.splitlines():
        line = raw.strip()
        if "-->" in line:
            start = line.split("-->")[0].strip()
            # start looks like HH:MM:SS.mmm or MM:SS.mmm
            clock = start.split(".")[0]
            bits = [int(b) for b in clock.split(":")]
            secs = 0
            for b in bits:
                secs = secs * 60 + b
            current_ts = _seconds_to_mmss(secs)
        elif line and not line.isdigit() and line != "WEBVTT" and current_ts:
            text = _TIMESTAMP_TAG_RE.sub("", line).strip()
            if text:
                lines.append(f"{current_ts}  {text}")
    return "\n".join(lines)


def fetch_transcript(video_id: str, timeout: float = 15.0) -> str | None:
    """Best-effort fetch of Loom's auto-generated transcript.

    Loom exposes an unauthenticated GraphQL endpoint for captions. This is an
    unofficial API, so any failure returns None - the pipeline then relies on
    Gemini's own audio transcription instead of failing.
    """
    query = {
        "operationName": "FetchVideoTranscript",
        "variables": {"videoId": video_id},
        "query": (
            "query FetchVideoTranscript($videoId: ID!) {"
            "  fetchVideoTranscript(videoId: $videoId) {"
            "    ... on VideoTranscriptDetails { captions_source_url } "
            "    __typename"
            "  }"
            "}"
        ),
    }
    try:
        resp = requests.post(_GRAPHQL_URL, json=query, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        details = (data.get("data") or {}).get("fetchVideoTranscript") or {}
        captions_url = details.get("captions_source_url")
        if not captions_url:
            return None
        vtt = requests.get(captions_url, timeout=timeout)
        vtt.raise_for_status()
        parsed = _parse_vtt(vtt.text)
        return parsed or None
    except (requests.RequestException, ValueError, KeyError):
        return None


def download_video(url: str, dest_dir: Path, video_id: str) -> Path:
    """Download the Loom MP4 with yt-dlp. Returns the path to the file."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(dest_dir / f"loom_{video_id}.%(ext)s")
    subprocess.run(
        [
            "yt-dlp",
            "--no-playlist",
            "--quiet",
            "--no-warnings",
            "-o",
            out_template,
            url,
        ],
        check=True,
    )
    produced = sorted(dest_dir.glob(f"loom_{video_id}.*"))
    if not produced:
        raise RuntimeError(f"yt-dlp did not produce a file for {url!r}")
    return produced[0]
