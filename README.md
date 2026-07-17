# loomnt

**Turn a Loom video into a to-do list.** Sometimes you just don't have five (or
twenty-five) minutes to watch a coworker's Loom — and that's okay. We love our coworkers.
We love their Looms. Loom walkthroughs are genuinely excellent briefings: rich, personal,
full of context you'd never get from a Slack message. But sometimes you'd trade all that
warmth for a crisp, to-the-point list of what you actually need to *do*.

`loomnt` watches the Loom so you don't have to, and hands you the list.

> To our beloved coworkers: we treasure your Looms. This tool exists purely so we can act
> on them faster, not so we can avoid them. (We'd never.) Think of it as turning a Loom
> into an email — with AI.

## Why this is more than a transcript

A plain transcript of a screen recording is often useless on its own. Half of what gets
said is *"turn this right here to that side"* or *"make this thing match that one"* —
pure gesture, meaningless without the picture. The speaker is pointing with their cursor
and the words only make sense if you can see where it's pointing.

`loomnt` reads **both** the words and the video. It watches where the cursor is and what's
on screen at each moment, so *"turn this right here to that side"* becomes a concrete task
like *"Move the Search bar to the far right of the Editor's top nav."* The vague becomes
specific.

That also makes it genuinely useful when you **can't** watch the video:

- **Accessibility** — for blind and low-vision folks, a spoken "click here" is a dead end.
  Grounding the narration in the on-screen context turns it into something readable and
  actionable.
- **Skimmers and the time-poor** — get the to-dos in ten seconds instead of ten minutes.
- **Loom skeptics** — you know who you are. We still love you. Here's your list.

## How it works

```
Loom URL
   │
   ├─ extract the 32-char video ID
   ├─ fetch Loom's transcript (best-effort, unofficial)
   ├─ download the MP4 with yt-dlp
   │
   ▼
Gemini (native video)  ── samples ~1 FPS + audio, watches the cursor over the UI
   │
   ▼
JSON action items  →  pretty terminal table + tasks.json
```

Gemini ingests the video natively — frames **and** audio — so it can follow the cursor at
each spoken moment and resolve "this" and "that" to real UI elements. If Loom's transcript
can't be fetched, Gemini transcribes the audio itself, so the tool still works.

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

You get a prioritized table in the terminal, plus a `tasks.json` array like:

```json
[
  {
    "task_name": "Reorder elements in the Editor's top navigation bar",
    "description": "- **Context**: The Editor page's top nav bar…\n- **Current Behavior**: …\n- **Expected Behavior**: Move the Search bar and status indicators to the far right…\n- **Timestamp Reference**: 00:34-01:38",
    "priority": "Normal",
    "tags": ["UI/UX", "Editor"],
    "timestamp": "00:34-01:38"
  }
]
```

Each task carries a **timestamp reference** back to the video, so if the list ever makes
you curious, you can jump straight to that moment and — yes — actually watch the Loom.

## Roadmap

- Claude refinement pass (polish titles/descriptions to your team's naming conventions).
- ClickUp task creation straight from the JSON output.

## Development

```bash
pip install -e ".[dev]"
pytest
```
