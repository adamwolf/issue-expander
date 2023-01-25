import pytest

import issue_expander
from issue_expander.expander import expandRefsToMarkdown


@pytest.mark.parametrize(
    "nonexpansion",
    [
        "http://www.github.com/adamwolf/issue-expander/issues/23",
        "http://github.com/adamwolf/issue-expander/issues/23",
        "https://www.github.com/adamwolf/issue-expander/issues/23",
        "https://github.com/adamwolf/issue-expander/issues/#23",
        "https://github.com/adamwolf/issue-expander/pull/#23",
        "https://github.com/adamwolf/issue-expander/issue/23",
        "https://github.com/adamwolf/issue-expander/pulls/23",
        "https://en.github.com/adamwolf/issue-expander/issues/23",
        "https://github.blog/adamwolf/issue-expander/issues/23",
        "https://github.org/adamwolf/issue-expander/issues/23",
        "https://github.org/adamwolf/issue-expander/pull/23",
    ],
)
def test_url_nonexpansion(nonexpansion, monkeypatch):
    """Many github urls should not be expanded."""

    def mockIssue(group, repository, number, username, token):
        raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(nonexpansion)
    assert expansion == nonexpansion


@pytest.mark.parametrize(
    "input_text,expectation",
    (
        (
            "https://github.com/adamwolf/faux-expander/issues/23",
            "[Detect url references #23]" "(https://github.com/adamwolf/faux-expander/issues/23)",
        ),
        (
            "https://github.com/adamwolf/faux-expander/pull/23",
            "[Detect url references #23]" "(https://github.com/adamwolf/faux-expander/issues/23)",
        ),
    ),
)
def test_url_expansion(input_text, expectation, monkeypatch):
    """A certain format of GitHub urls should be expanded."""

    def mockIssue(group, repository, number, username, token):
        if (
            group == "adamwolf"
            and repository == "faux-expander"
            and number == "23"
            and username is None
            and token is None
        ):
            return {
                "html_url": "https://github.com/adamwolf/faux-expander/issues/23",
                "title": "Detect url references",
            }

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown(input_text)
    assert expansion == expectation


def test_gitlab_urls():
    """GitLab urls should not be expanded... (yet!)"""
    for input_text in (
        "https://gitlab.com/adamwolf/issue-expander/issues/23",
        "https://gitlab.com/adamwolf/issue-expander/pull/23",
    ):
        expansion = expandRefsToMarkdown(input_text)
        assert expansion == input_text
