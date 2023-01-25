import io
import json
from unittest.mock import patch
from urllib.error import HTTPError

import issue_expander
from issue_expander.expander import getIssue


def test_getIssue_with_404(monkeypatch):
    """getIssue should return None if the issue is not found"""

    def mock_urlopen(request, context=None):
        raise HTTPError("http://example.com", 404, "Not Found", {}, io.BytesIO(b""))

    monkeypatch.setattr(issue_expander.expander, "urlopen", mock_urlopen)
    assert getIssue("adamwolf", "issue-expander", "1", None, None) is None


def test_getIssue_puts_token_in_headers():
    """getIssue should put the token in the headers as Authorization"""

    with patch(
        "issue_expander.expander.urlopen",
        return_value=io.BytesIO(json.dumps({"html_url": "foo", "title": "bar"}).encode("utf-8")),
    ) as mock_urlopen:
        assert getIssue("adamwolf", "issue-expander", "1", None, "frobnitz") == {
            "html_url": "foo",
            "title": "bar",
        }
        mock_urlopen.assert_called_once
        request_headers = mock_urlopen.call_args[0][0].headers
        assert request_headers["Authorization"] == "Bearer: frobnitz"


def test_getIssue_with_403_without_token(monkeypatch, capsys):
    """getIssue should return None but print an error if GitHub rate limits us.

    If we didn't pass a token it, it should tell us to try again with a token."""

    def mock_urlopen(request, context=None):
        raise HTTPError("http://example.com", 403, "Rate limit exceeded.", {}, io.BytesIO(b""))

    monkeypatch.setattr(issue_expander.expander, "urlopen", mock_urlopen)
    assert getIssue("adamwolf", "issue-expander", "1", None, None) is None
    captured = capsys.readouterr()
    assert (
        captured.err
        == "Unable to look up issue due to rate limit error. Try providing a token with --token.\n"
    )


def test_getIssue_with_403_with_token(monkeypatch, capsys):
    """getIssue should return None but print an error if GitHub rate limits us.

    If we passed a token in, it shouldn't tell us to try again with a token."""

    def mock_urlopen(request, context=None):
        raise HTTPError("http://example.com", 403, "Rate limit exceeded.", {}, io.BytesIO(b"foo   "))

    monkeypatch.setattr(issue_expander.expander, "urlopen", mock_urlopen)
    assert getIssue("adamwolf", "issue-expander", "1", None, "imatoken") is None
    captured = capsys.readouterr()
    assert captured.err == "Unable to look up issue due to rate limit error.\n"


def test_getIssue_with_malformed_json(monkeypatch, capsys):
    """getIssue should return None and print an error if the JSON is malformed"""

    def mock_urlopen(request, context=None):
        raise json.JSONDecodeError("msg", "doc", 0)

    monkeypatch.setattr(issue_expander.expander, "urlopen", mock_urlopen)
    assert getIssue("adamwolf", "issue-expander", "1", None, None) is None

    captured = capsys.readouterr()

    assert (
        captured.err
        == "Unable to parse response from https://api.github.com/repos/adamwolf/issue-expander/issues/1\n"
    )


def test_getIssue_happy_path():
    """getIssue should return the issue if it's found"""

    with patch(
        "issue_expander.expander.urlopen",
        return_value=io.BytesIO(json.dumps({"html_url": "foo", "title": "bar"}).encode("utf-8")),
    ) as mock_urlopen:
        assert getIssue("adamwolf", "issue-expander", "1", None, None) == {
            "html_url": "foo",
            "title": "bar",
        }
        mock_urlopen.assert_called_once
