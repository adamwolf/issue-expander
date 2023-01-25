import io
import json
from unittest.mock import patch

from issue_expander.expander import expandRefsToMarkdown


def test_issue_lookups_are_cached_in_a_line():
    """A line with multiple references to the same issue should only make one API call."""

    def mock_urlopen(*args, **kwargs):
        return io.BytesIO(
            json.dumps(
                {"html_url": "https://example.com/pulls/101", "title": "Meow, meow, I'm a cow"}
            ).encode("utf-8")
        )

    with patch("issue_expander.expander.urlopen", side_effect=mock_urlopen) as mock_urlopen:

        expansion = expandRefsToMarkdown("adamwolf/geewhiz#101 adamwolf/geewhiz#101")
        expected = (
            "[Meow, meow, I'm a cow #101](https://example.com/pulls/101) "
            "[Meow, meow, I'm a cow #101](https://example.com/pulls/101)"
        )

        assert expansion == expected
        assert mock_urlopen.call_count == 1


def test_issue_lookups_are_cached_across_lines():
    """A line with multiple references to the same issue should only make one API call."""

    def mock_urlopen(*args, **kwargs):
        return io.BytesIO(
            json.dumps(
                {"html_url": "https://example.com/pulls/101", "title": "Meow, meow, I'm a cow"}
            ).encode("utf-8")
        )

    with patch("issue_expander.expander.urlopen", side_effect=mock_urlopen) as mock_urlopen:

        expansion = expandRefsToMarkdown("adamwolf/geewhiz#101\nadamwolf/geewhiz#101\nadamwolf/geewhiz#101")
        expected = (
            "[Meow, meow, I'm a cow #101](https://example.com/pulls/101)\n"
            "[Meow, meow, I'm a cow #101](https://example.com/pulls/101)\n"
            "[Meow, meow, I'm a cow #101](https://example.com/pulls/101)"
        )

        assert expansion == expected
        assert mock_urlopen.call_count == 1
