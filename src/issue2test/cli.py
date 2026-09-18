from __future__ import annotations

import argparse
from pathlib import Path

from .core import generate_test


def _read_issue(args: argparse.Namespace) -> str:
    if args.issue:
        return args.issue
    if args.issue_file:
        return Path(args.issue_file).read_text(encoding="utf-8")
    raise SystemExit("Provide --issue or --issue-file.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="issue2test",
        description="Generate a pytest regression test from a bug report.",
    )
    parser.add_argument("--issue", help="Bug report text.")
    parser.add_argument("--issue-file", help="Path to a text file containing the bug report.")
    parser.add_argument("--source", required=True, help="Path to the relevant Python source file.")
    parser.add_argument("--output", help="Optional path to write the generated test.")
    parser.add_argument("--model", help="OpenAI model override.")
    args = parser.parse_args()

    source_path = Path(args.source)
    source = source_path.read_text(encoding="utf-8")
    issue = _read_issue(args)

    result = generate_test(
        issue=issue,
        source=source,
        source_path=str(source_path),
        model=args.model,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result + "\n", encoding="utf-8")
        print(f"Wrote generated test to {output_path}")
    else:
        print(result)


if __name__ == "__main__":
    main()
