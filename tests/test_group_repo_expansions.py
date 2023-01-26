import pytest

import issue_expander
from issue_expander.expander import expandRefsToMarkdown


@pytest.mark.parametrize(
    "input_text,expectation",
    (
        ("foo/bar#100", "[Example Issue #100](https://github.com/foo/bar/issues/100)"),
        (
            "              foo/bar#100",
            "              [Example Issue #100](https://github.com/foo/bar/issues/100)",
        ),
        ("\n\nfoo/bar#100\n", "\n\n[Example Issue #100](https://github.com/foo/bar/issues/100)\n"),
    ),
)
def test_group_repo_issue_expansion(input_text, expectation, monkeypatch):
    """Issue references should be expanded"""

    def mockIssue(group, repository, number, token):
        if group == "foo" and repository == "bar" and number == "100" and token is None:
            return {
                "html_url": "https://github.com/foo/bar/issues/100",
                "title": "Example Issue",
            }
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(input_text)
    assert expansion == expectation


@pytest.mark.parametrize(
    "nonexpansion",
    [
        "foo /bar#100",
        "foo/ bar#100",
        "foo /bar#100",
        "foo/bar #100",
        "!!!!!/bar#100",
        "bar/!!!!!!!!#100",
        "foo//bar#100",
        "foo/bar/#100",
    ],
)
def test_group_repo_nonexpansion(nonexpansion, monkeypatch):
    """Many GitHub urls should not be expanded."""

    def mockIssue(group, repository, number, token):
        if group == "foo" and repository == "bar" and number == "100" and token is None:
            return {"html_url": "https://github.com/foo/bar/issues/100", "title": "Example Issue"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(nonexpansion)
    assert expansion == nonexpansion
