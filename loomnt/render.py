"""Output rendering: a terminal table and a JSON file."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .models import Task

_PRIORITY_STYLE = {"High": "bold red", "Normal": "yellow", "Low": "dim"}


def print_table(tasks: list[Task]) -> None:
    console = Console()
    if not tasks:
        console.print("[dim]No actionable tasks found in this video.[/dim]")
        return

    table = Table(title=f"Action items ({len(tasks)})", show_lines=True)
    table.add_column("Priority", no_wrap=True)
    table.add_column("Task", style="bold")
    table.add_column("Tags")
    table.add_column("Time", no_wrap=True)

    for task in tasks:
        style = _PRIORITY_STYLE.get(task.priority, "")
        table.add_row(
            f"[{style}]{task.priority}[/{style}]" if style else task.priority,
            task.task_name,
            ", ".join(task.tags),
            task.timestamp,
        )
    console.print(table)


def write_json(tasks: list[Task], path: Path) -> None:
    payload = [task.model_dump() for task in tasks]
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
