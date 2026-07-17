"""Gemini video analysis: upload the MP4, run the prompt, return structured tasks."""

from __future__ import annotations

import os
import time
from pathlib import Path

from google import genai
from google.genai import types

from .models import Task
from .prompt import build_prompt

DEFAULT_MODEL = "gemini-2.5-pro"


def analyze(
    video_path: Path,
    transcript: str | None,
    model: str | None = None,
) -> list[Task]:
    """Upload the video to Gemini and return the decoded action items."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your environment or a .env file."
        )

    client = genai.Client(api_key=api_key)
    model = model or os.environ.get("GEMINI_MODEL") or DEFAULT_MODEL

    uploaded = client.files.upload(file=str(video_path))

    # Video files are processed asynchronously; wait until ACTIVE.
    while uploaded.state and uploaded.state.name == "PROCESSING":
        time.sleep(3)
        uploaded = client.files.get(name=uploaded.name)

    if uploaded.state and uploaded.state.name == "FAILED":
        raise RuntimeError("Gemini failed to process the uploaded video.")

    response = client.models.generate_content(
        model=model,
        contents=[uploaded, build_prompt(transcript)],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[Task],
        ),
    )

    tasks = response.parsed
    if tasks is None:
        # Fall back to manual JSON parsing if the SDK didn't auto-parse.
        import json

        raw = json.loads(response.text or "[]")
        tasks = [Task(**item) for item in raw]
    return tasks
