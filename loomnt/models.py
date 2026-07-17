"""Structured output schema for extracted action items."""

from typing import Literal

from pydantic import BaseModel, Field


class Task(BaseModel):
    """A single, concrete engineering action item decoded from the video."""

    task_name: str = Field(
        description="A short, descriptive, action-oriented title, e.g. "
        "'Fix alignment of dashboard export button'."
    )
    description: str = Field(
        description=(
            "A comprehensive markdown description containing:\n"
            "- **Context**: what page/UI component is being discussed.\n"
            "- **Current Behavior**: what the video shows / what the user complains about.\n"
            "- **Expected Behavior**: the specific technical change requested.\n"
            "- **Timestamp Reference**: the exact MM:SS range in the video."
        )
    )
    priority: Literal["High", "Normal", "Low"] = Field(
        description="Inferred from the speaker's urgency and the impact on UX."
    )
    tags: list[str] = Field(
        description="e.g. bug, feature-request, UI/UX, tech-debt."
    )
    timestamp: str = Field(
        description="The MM:SS or MM:SS-MM:SS range in the video this task refers to."
    )
