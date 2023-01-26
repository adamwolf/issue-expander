import pytest

import issue_expander
from issue_expander.expander import expandRefsToMarkdown


@pytest.mark.parametrize(
    "input_text,expectation",
    (
        ("GH-100", "[Example Issue #100](https://github.com/foo/bar/issues/100)"),
        (
            "              GH-100",
            "              [Example Issue #100](https://github.com/foo/bar/issues/100)",
        ),
        ("\n\nGH-100\n", "\n\n[Example Issue #100](https://github.com/foo/bar/issues/100)\n"),
    ),
)
def test_gh_issue_expansion(input_text, expectation, monkeypatch):
    """Issue references like GH-32 should be expanded"""

    def mockIssue(group, repository, number, token):
        if group == "foo" and repository == "bar" and number == "100" and token is None:
            return {"html_url": "https://github.com/foo/bar/issues/100", "title": "Example Issue"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(input_text, default_group="foo", default_repository="bar")
    assert expansion == expectation


@pytest.mark.parametrize(
    "nonexpansion",
    ["GH 100", "G H-100", "G-H-100", "GH- 100", "GH-#100", "GH_100", "GGHH-100", "100-GH", "UGH-100"],
)
def test_gh_nonexpansion(nonexpansion, monkeypatch):
    """Many things with GH in them should not be expanded."""

    def mockIssue(group, repository, number, token):
        if group == "foo" and repository == "privaterepo" and number == "555" and token == "password1":
            return {"html_url": "https://example.com/pulls/555", "title": "Sshhh!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(nonexpansion, default_group="foo", default_repository="bar")
    assert expansion == nonexpansion
