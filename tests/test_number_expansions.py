import re

import pytest
import responses

from issue_expander.issue_expander import expandRefsToMarkdown


@responses.activate
@pytest.mark.parametrize(
    "input_text,expectation",
    (
        ("#100", "[Example Issue #100](https://github.com/foo/bar/issues/100)"),
        ("              #100", "              [Example Issue #100](https://github.com/foo/bar/issues/100)"),
        ("\n\n#100\n", "\n\n[Example Issue #100](https://github.com/foo/bar/issues/100)\n"),
    ),
)
def test_number_issue_expansion(input_text, expectation):
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
def test_number_nonexpansion(nonexpansion):
    """Many things with numbers in them should not be expanded."""
    rsp = responses.get(re.compile("http.*"))

    expansion = expandRefsToMarkdown(nonexpansion, default_group="foo", default_repository="bar")
    assert expansion == nonexpansion

    assert rsp.call_count == 0