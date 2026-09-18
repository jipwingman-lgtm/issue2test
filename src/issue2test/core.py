from __future__ import annotations

import os

from openai import OpenAI


INSTRUCTIONS = """You are an expert Python test engineer.
Generate one focused pytest regression test for the reported bug.
Use only behavior and interfaces supported by the supplied source.
Do not modify production code.
Prefer the smallest test that demonstrates the bug or expected behavior.
Return only Python test code with no Markdown fences or commentary.
"""


def build_prompt(issue: str, source: str, source_path: str = "source.py") -> str:
    issue = issue.strip()
    source = source.strip()

    if not issue:
        raise ValueError("issue must not be empty")
    if not source:
        raise ValueError("source must not be empty")

    return (
        "BUG REPORT:\n"
        f"{issue}\n\n"
        f"SOURCE FILE: {source_path}\n"
        "-----\n"
        f"{source}\n"
        "-----\n\n"
        "Write a pytest regression test for this bug."
    )


def _strip_markdown_fence(text: str) -> str:
    text = text.strip()
    fence = chr(96) * 3
    if text.startswith(fence) and text.endswith(fence):
        lines = text.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    return text


def generate_test(
    issue: str,
    source: str,
    source_path: str = "source.py",
    model: str | None = None,
) -> str:
    model = model or os.getenv("OPENAI_MODEL", "gpt-5.3-codex")
    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=build_prompt(issue, source, source_path),
    )

    return _strip_markdown_fence(response.output_text)
