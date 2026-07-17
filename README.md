# loomnt

Turn a **Loom video URL** into a list of concrete engineering **action items**.

Roberto records Loom walkthroughs where he points at the screen and speaks vaguely —
"make *this* blue", "fix *that* alignment". `loomnt` watches the video and reads the
transcript, then decodes each vague reference by cross-referencing the spoken words
against what the mouse cursor is pointing at on screen, and emits a structured task list.

## How it works

```
Loom URL
   │
   ├─ extract 32-char video ID
   ├─ fetch Loom's transcript (best-effort, unofficial GraphQL)
   ├─ download the MP4 with yt-dlp
   │
   ▼
Gemini (native video)  ── samples ~1 FPS + audio, sees the cursor over the UI
   │
   ▼
JSON action items  →  pretty terminal table + tasks.json
```

Gemini ingests the video natively (frames **and** audio), so it can watch the cursor at
each spoken moment — no manual frame extraction needed. If Loom's transcript can't be
fetched, Gemini transcribes the audio itself, so the tool still works.

## Install

Requires Python 3.10+ and [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) on your PATH.

```bash
pip install -e .
```

## Setup

```bash
cp .env.example .env
# then edit .env and set GEMINI_API_KEY
```

## Usage

```bash
loomnt https://www.loom.com/share/<video-id>
loomnt https://www.loom.com/share/<video-id> --out my-tasks.json
loomnt https://www.loom.com/share/<video-id> --model gemini-2.5-pro
```

Output: a table of prioritized tasks in the terminal, plus a `tasks.json` array like:

```json
[
  {
    "task_name": "Fix alignment of dashboard export button",
    "description": "- **Context**: Dashboard header…\n- **Current Behavior**: …\n- **Expected Behavior**: …\n- **Timestamp Reference**: 01:12-01:20",
    "priority": "High",
    "tags": ["bug", "UI/UX"],
    "timestamp": "01:12-01:20"
  }
]
```

## Roadmap

- Claude refinement pass (polish titles/descriptions to naming conventions).
- ClickUp task creation from the JSON output.

## Development

```bash
pip install -e ".[dev]"
pytest
```
