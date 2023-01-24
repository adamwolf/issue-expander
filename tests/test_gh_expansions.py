import re

import pytest
import responses

from issue_expander.issue_expander import expandRefsToMarkdown


@responses.activate
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
def test_gh_issue_expansion(input_text, expectation):
    """Issue references should be expanded"""
    responses.get(
        "https://api.github.com/repos/foo/bar/issues/100",
        json={
            "html_url": "https://github.com/foo/bar/issues/100",
            "title": "Example Issue",
        },
    )

    expansion = expandRefsToMarkdown(input_text, default_group="foo", default_repository="bar")
    assert expansion == expectation


@responses.activate
@pytest.mark.parametrize(
    "nonexpansion",
    ["GH 100", "G H-100", "G-H-100", "GH- 100", "GH-#100", "GH_100", "GGHH-100", "100-GH", "UGH-100"],
)
def test_gh_nonexpansion(nonexpansion):
    """Many things with GH in them should not be expanded."""
    rsp = responses.get(re.compile("http.*"))

    expansion = expandRefsToMarkdown(nonexpansion, default_group="foo", default_repository="bar")
    assert expansion == nonexpansion

    assert rsp.call_count == 0
