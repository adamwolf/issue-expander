import re

import pytest
import responses

from issue_expander.issue_expander import expandRefsToMarkdown


@responses.activate
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
def test_url_nonexpansion(nonexpansion):
    """Many github urls should not be expanded."""
    rsp = responses.get(re.compile("http.*"))

    expansion = expandRefsToMarkdown(nonexpansion)
    assert expansion == nonexpansion

    assert rsp.call_count == 0


@responses.activate
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
def test_url_expansion(input_text, expectation):
    """A certain format of GitHub urls should be expanded."""
    responses.get(
        "https://api.github.com/repos/adamwolf/faux-expander/issues/23",
        json={
            "html_url": "https://github.com/adamwolf/faux-expander/issues/23",
            "title": "Detect url references",
        },
    )

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
