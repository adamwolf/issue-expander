import pytest

import issue_expander
from issue_expander.expander import expandRefsToMarkdown


@pytest.mark.parametrize(
    "input_text,expectation",
    (
        ("#100", "[Example Issue #100](https://github.com/foo/bar/issues/100)"),
        ("              #100", "              [Example Issue #100](https://github.com/foo/bar/issues/100)"),
        ("\n\n#100\n", "\n\n[Example Issue #100](https://github.com/foo/bar/issues/100)\n"),
    ),
)
def test_number_issue_expansion(input_text, expectation, monkeypatch):
    """Issue references should be expanded"""

    def mockIssue(group, repository, number, username, token):
        if (
            group == "foo"
            and repository == "bar"
            and number == "100"
            and username is None
            and token is None
        ):
            return {
                "html_url": "https://github.com/foo/bar/issues/100",
                "title": "Example Issue",
            }
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(input_text, default_group="foo", default_repository="bar")
    assert expansion == expectation


@pytest.mark.parametrize(
    "nonexpansion",
    [
        "# 100",
        "100",
        "#100#",
        "#!100",
        "HELLO#100",
        "100#",
        "#.100",
    ],
)
def test_number_nonexpansion(nonexpansion, monkeypatch):
    """Many things with numbers in them should not be expanded."""

    def mockIssue(group, repository, number, username, token):
        raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(nonexpansion, default_group="foo", default_repository="bar")
    assert expansion == nonexpansion
