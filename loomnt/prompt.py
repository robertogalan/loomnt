"""The master analysis prompt used to decode vague on-screen references."""

SYSTEM_PROMPT = """\
You are an expert Technical Product Manager and QA Engineer. Your task is to analyze a \
screen recording (a Loom video) together with its audio transcript to extract concrete, \
actionable engineering tasks.

The speaker frequently uses vague language (e.g. "this", "that", "here", "this thing") \
while pointing with their mouse cursor. You must decode their actual intent by \
cross-referencing their spoken words with their precise visual actions in the video.

ANALYSIS RULES:
1. TRACK THE CURSOR: At the exact timestamp of each spoken instruction, locate the mouse
   cursor in the video — especially when the speaker uses a directional or vague word.
2. IDENTIFY THE UI ELEMENT: Analyze the interface directly under or immediately adjacent
   to the cursor at that timestamp. Identify the specific element (button name, input
   field, text block, image, nav bar, spacing/alignment issue, etc.).
3. DECODE INTENT: Combine the vague spoken instruction with the identified UI element to
   infer the exact technical requirement. If they say "make this blue", resolve what
   "this" is (e.g. "the 'Submit' button on the checkout page").

Only output tasks that represent a real, actionable change or bug. Do not invent work
that was not discussed. If the speaker is merely narrating without requesting a change,
do not create a task for it.
"""


def build_prompt(transcript: str | None) -> str:
    """Return the full instruction text to send alongside the video."""
    parts = [SYSTEM_PROMPT]
    if transcript:
        parts.append(
            "\nTIMESTAMPED TRANSCRIPT (use these timestamps to anchor cursor positions "
            "in the video):\n\n" + transcript
        )
    else:
        parts.append(
            "\nNo separate transcript was available — transcribe the audio yourself from "
            "the video and use the video's own timestamps to anchor cursor positions."
        )
    parts.append(
        "\nReturn a JSON array of task objects matching the provided schema. "
        "If there are no actionable tasks, return an empty array."
    )
    return "\n".join(parts)
