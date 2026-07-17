"""Command-line entry point: loom URL -> action-item list."""

from __future__ import annotations

import tempfile
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from . import gemini, loom, render

_console = Console(stderr=True)


@click.command()
@click.argument("url")
@click.option(
    "--out",
    default="tasks.json",
    show_default=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Where to write the JSON array of tasks.",
)
@click.option(
    "--model",
    default=None,
    help="Gemini model override (must support video). "
    "Defaults to $GEMINI_MODEL or gemini-2.5-pro.",
)
def main(url: str, out: Path, model: str | None) -> None:
    """Analyze a Loom video URL and produce a list of engineering action items."""
    load_dotenv()

    video_id = loom.extract_video_id(url)
    _console.print(f"[dim]Video ID:[/dim] {video_id}")

    _console.print("[dim]Fetching transcript…[/dim]")
    transcript = loom.fetch_transcript(video_id)
    _console.print(
        "[dim]  transcript found[/dim]"
        if transcript
        else "[dim]  no native transcript — Gemini will transcribe audio[/dim]"
    )

    with tempfile.TemporaryDirectory(prefix="loomnt_") as tmp:
        _console.print("[dim]Downloading video…[/dim]")
        video_path = loom.download_video(url, Path(tmp), video_id)

        _console.print("[dim]Analyzing with Gemini (this can take a minute)…[/dim]")
        tasks = gemini.analyze(video_path, transcript, model)

    render.print_table(tasks)
    render.write_json(tasks, out)
    _console.print(f"[green]Wrote {len(tasks)} task(s) to[/green] {out}")


if __name__ == "__main__":
    main()
