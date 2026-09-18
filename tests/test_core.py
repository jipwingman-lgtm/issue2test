import pytest

from issue2test.core import _strip_markdown_fence, build_prompt


def test_build_prompt_contains_issue_and_source():
    prompt = build_prompt(
        "divide(1, 0) should raise ValueError",
        "def divide(a, b):\n    return a / b",
        "calculator.py",
    )

    assert "divide(1, 0) should raise ValueError" in prompt
    assert "calculator.py" in prompt
    assert "def divide(a, b):" in prompt


@pytest.mark.parametrize("issue,source", [("", "x = 1"), ("bug", "")])
def test_build_prompt_rejects_empty_inputs(issue, source):
    with pytest.raises(ValueError):
        build_prompt(issue, source)


def test_strip_markdown_fence():
    fence = chr(96) * 3
    fenced = fence + "python\ndef test_example():\n    assert True\n" + fence
    assert _strip_markdown_fence(fenced) == "def test_example():\n    assert True"
