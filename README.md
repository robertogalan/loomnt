<p align="center">
  <img src="assets/loomnt.png" alt="loomnt" width="180">
</p>

# loomn't

**Turn a Loom video into a to-do list.** Sometimes you just don't have five (or
twenty-five) minutes to watch a coworker's Loom - and that's okay. We love our coworkers.
We love their Looms. Loom walkthroughs are genuinely excellent briefings: rich, personal,
full of context you'd never get from a Slack message. But sometimes you'd trade all that
warmth for a crisp, to-the-point list of what you actually need to *do*.

`loomnt` watches the Loom so you don't have to, and hands you the list.

> To our beloved coworkers: we treasure your Looms. This tool exists purely so we can act
> on them faster, not so we can avoid them. (We'd never.) Think of it as turning a Loom
> into an email - with AI.

## Why this is more than a transcript

A plain transcript of a screen recording is often useless on its own. Half of what gets
said is *"turn this right here to that side"* or *"make this thing match that one"* -
pure gesture, meaningless without the picture. The speaker is pointing with their cursor
and the words only make sense if you can see where it's pointing.

`loomnt` reads **both** the words and the video. It watches where the cursor is and what's
on screen at each moment, so *"turn this right here to that side"* becomes a concrete task
like *"Move the Search bar to the far right of the Editor's top nav."* The vague becomes
specific.

That also makes it genuinely useful when you **can't** watch the video:

- **Accessibility** - for blind and low-vision folks, a spoken "click here" is a dead end.
  Grounding the narration in the on-screen context turns it into something readable and
  actionable.
- **Skimmers and the time-poor** - get the to-dos in ten seconds instead of ten minutes.
- **Loom skeptics** - you know who you are. We still love you. Here's your list.

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

Gemini ingests the video natively - frames **and** audio - so it can follow the cursor at
each spoken moment and resolve "this" and "that" to real UI elements. If Loom's transcript
can't be fetched, Gemini transcribes the audio itself, so the tool still works.

## Install

All options need [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) on your PATH
(`brew install yt-dlp`, `pipx install yt-dlp`, or `sudo apt install yt-dlp`).

### Quickest - pipx (Linux / macOS / Windows)

One command, isolated, cross-platform (requires Python 3.10+ and
[pipx](https://pipx.pypa.io)):

```bash
pipx install git+https://github.com/robertogalan/loomnt.git
```

### Prebuilt binary (no Python needed)

Grab a standalone executable for your OS from the
[**Releases**](https://github.com/robertogalan/loomnt/releases) page
(Linux / macOS / Windows), make it executable, and run it. You still need `yt-dlp`
installed.

### From source (for development)

```bash
git clone https://github.com/robertogalan/loomnt.git
cd loomnt

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e .
```

## Set your Gemini API key

`loomnt` uses Google's Gemini to watch the video, so it needs a **Gemini API key**.

1. Get one for free at **[Google AI Studio → API keys](https://aistudio.google.com/apikey)**
   (click *Create API key*). It looks like `AIza…` or `AQ.…`.
2. Tell `loomnt` about it, either way:

   **Option A - a `.env` file.** `loomnt` reads a `.env` file in the directory you run it
   from. Create one with your key:
   ```bash
   echo "GEMINI_API_KEY=your-real-key-here" > .env
   ```
   Keep that `.env` out of version control. If you cloned this repo, its `.gitignore`
   already lists `.env`, so it won't be committed; anywhere else, make sure your own
   `.gitignore` covers it (or just use Option B).

   **Option B - an environment variable (simplest for pipx/binary installs):**
   ```bash
   export GEMINI_API_KEY=your-real-key-here
   ```

## Usage

Every session, activate the venv first, then run `loomnt` with a Loom share URL:

```bash
source .venv/bin/activate
loomnt https://www.loom.com/share/<video-id>
```

More options:

```bash
loomnt https://www.loom.com/share/<video-id> --out my-tasks.json   # custom output file
loomnt https://www.loom.com/share/<video-id> --model gemini-2.5-pro # override the model
loomnt --help                                                       # see all options
```

You get a prioritized table in the terminal plus a `tasks.json` array in the current
folder, like:

```json
[
  {
    "task_name": "Make the checkout 'Pay now' button use the brand teal",
    "description": "- **Context**: The checkout page's payment step.\n- **Current Behavior**: The narrator waves the cursor and says \"make this one pop\" - the 'Pay now' button is the default grey and blends into the page.\n- **Expected Behavior**: Recolor the 'Pay now' button to the brand teal (#00C2A8) so it reads as the primary action.\n- **Timestamp Reference**: 00:42-00:58",
    "priority": "Normal",
    "tags": ["UI/UX", "checkout"],
    "timestamp": "00:42-00:58"
  }
]
```

Each task carries a **timestamp reference** back to the video, so if the list ever makes
you curious, you can jump straight to that moment and - yes - actually watch the Loom.

## Roadmap

- Claude refinement pass (polish titles/descriptions to your team's naming conventions).
- ClickUp task creation straight from the JSON output.

## Development

```bash
pip install -e ".[dev]"
pytest
```
