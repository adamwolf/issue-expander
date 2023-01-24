import re

import pytest
import responses

from issue_expander.issue_expander import expandRefsToMarkdown


@responses.activate
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
def test_group_repo_issue_expansion(input_text, expectation):
    """Issue references should be expanded"""
    responses.get(
        "https://api.github.com/repos/foo/bar/issues/100",
        json={
            "html_url": "https://github.com/foo/bar/issues/100",
            "title": "Example Issue",
        },
    )

    expansion = expandRefsToMarkdown(input_text)
    assert expansion == expectation


@responses.activate
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
def test_group_repo_nonexpansion(nonexpansion):
    """Many github urls should not be expanded."""
    rsp = responses.get(re.compile("http.*"))

    expansion = expandRefsToMarkdown(nonexpansion)
    assert expansion == nonexpansion

    assert rsp.call_count == 0
