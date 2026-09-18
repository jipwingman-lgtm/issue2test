# Issue2Test

Issue2Test is an early-stage open-source CLI that turns a bug report and a Python source file into a focused pytest regression test using OpenAI coding models.

The goal is simple: help maintainers turn reproducible bug reports into tests faster, so fixes are easier to verify and regressions are easier to prevent.

## Status

Early prototype. The current version supports a single Python source file plus a text bug report. Contributions and feedback are welcome.

## Quick start

~~~bash
git clone https://github.com/jipwingman-lgtm/issue2test.git
cd issue2test
python -m venv .venv
source .venv/bin/activate
pip install -e .
export OPENAI_API_KEY="your-key"
issue2test --issue "Calling divide(1, 0) should raise ValueError" --source examples/calculator.py
~~~

By default, Issue2Test uses gpt-5.3-codex. You can override it with OPENAI_MODEL.

You can also save the generated test:

~~~bash
issue2test --issue-file bug.txt --source src/package/module.py --output tests/test_regression.py
~~~

## What it does

1. Reads a bug report.
2. Reads the relevant Python source file.
3. Builds a constrained test-generation prompt.
4. Calls the OpenAI Responses API.
5. Returns plain pytest code suitable for review.

Issue2Test does not automatically modify production code. Generated tests should always be reviewed before committing.

## Why this project

Small open-source projects often receive useful bug reports but have limited maintainer time. A regression test is one of the most valuable artifacts a bug report can produce: it captures expected behavior and helps prevent the same failure from returning.

## Roadmap

- [x] Single-file Python + pytest prototype
- [ ] Accept GitHub issue URLs
- [ ] Select relevant repository files automatically
- [ ] Generate tests across multi-file projects
- [ ] Add repository-aware validation in a sandbox
- [ ] Post draft test patches to pull requests
- [ ] Evaluate generated tests against a public benchmark of real bug reports

## Development

~~~bash
pip install -e ".[dev]"
pytest
~~~

## Contributing

Issues and pull requests are welcome. Please keep bug reports reproducible and avoid including secrets, credentials, or private source code.

## License

MIT
