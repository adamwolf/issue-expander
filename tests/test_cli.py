"""
Use the CLI directly for some high-level integration tests.
"""
import pytest
from click.testing import CliRunner

import issue_expander
from issue_expander.expander import cli


def test_file(monkeypatch):
    """Use a file as input."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/106970", "title": "Foobar the Frobnitz"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("adamwolf/geewhiz#101")

        result = runner.invoke(cli, ["hello.txt"])
        assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
        assert result.exit_code == 0


def test_stdin(monkeypatch):
    """Read input from stdin if given - as the input file."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/106970", "title": "Foobar the Frobnitz"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101")
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0


def test_gh_expansion(monkeypatch):
    """Expand GH-123 style references."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "123" and token is None:
            return {"html_url": "https://example.com/pull/123", "title": "Hoist the Mainsail!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["--default-source", "adamwolf/geewhiz", "-"], input="GH-123")
    assert result.output == "[Hoist the Mainsail! #123](https://example.com/pull/123)"
    assert result.exit_code == 0


def test_url_expansion(monkeypatch):
    """Expand url references."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "123" and token is None:
            return {"html_url": "https://example.com/pull/123", "title": "Hoist the Mainsail!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="https://github.com/adamwolf/geewhiz/pull/123")
    assert result.output == "[Hoist the Mainsail! #123](https://example.com/pull/123)"
    assert result.exit_code == 0


def test_url_expansion_with_mismatched_urls(monkeypatch):
    """Expand url references when the url is for an issue and the item is a PR."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "123" and token is None:
            return {"html_url": "https://example.com/pulls/123", "title": "Hoist the Mainsail!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="https://github.com/adamwolf/geewhiz/issues/123")
    assert result.output == "[Hoist the Mainsail! #123](https://example.com/pulls/123)"
    assert result.exit_code == 0


def test_default_source(monkeypatch):
    """Use a default group/repository when specified as an option."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/106970", "title": "Foobar the Frobnitz"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["--default-source", "adamwolf/geewhiz", "-"], input="#101")
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0


bad_default_sources = [
    "",
    "https://www.google.com",
    "      adamwolf/geewhiz",
    "adamwolf     /      geewhiz",
    "adamwolf",
    "adamwolf/",
    "/geewhiz",
    "adamwolf/geewhiz/",
    "adamwolf//geewhiz",
    "/" "//" "a/b/c" " hello world" "01189998819991197253",
]


@pytest.mark.parametrize("source", bad_default_sources)
def test_malformed_default_sources(source):
    """Malformed default sources are rejected with a usage error."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--default-source", source, "-"], input="#101")
    assert result.exit_code == 1
    assert "Error: default source must be in the format 'group/repository'\n" in result.output


def test_default_source_but_not_needed(monkeypatch):
    """Don't override a specified group/repository even if a default is specified"""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/106970", "title": "Foobar the Frobnitz"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--default-source", "adamwolf/defaultdefault", "-"],
        input="adamwolf/geewhiz#101",
    )
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0


def test_two_expansions_in_one_line(monkeypatch):
    """Test that we can expand multiple issues in one line"""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/101", "title": "Foobar the Frobnitz"}
        elif group == "adamwolf" and repository == "geewhiz" and number == "102" and token is None:
            return {"html_url": "https://example.com/pulls/102", "title": "HOTFIX: fix the frobnitz!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101 adamwolf/geewhiz#102")
    assert result.output == (
        "[Foobar the Frobnitz #101](https://example.com/pulls/101) "
        "[HOTFIX: fix the frobnitz! #102](https://example.com/pulls/102)"
    )


def test_multiline_expansions_over_stdin(monkeypatch):
    """Expand issues on each line when given multiple lines through stdin"""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/101", "title": "Foobar the Frobnitz"}
        elif group == "adamwolf" and repository == "geewhiz" and number == "102" and token is None:
            return {"html_url": "https://example.com/pulls/102", "title": "HOTFIX: fix the frobnitz!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101\nhello world\nadamwolf/geewhiz#102")
    assert result.output == (
        "[Foobar the Frobnitz #101](https://example.com/pulls/101)\n"
        "hello world\n"
        "[HOTFIX: fix the frobnitz! #102](https://example.com/pulls/102)"
    )
    assert result.exit_code == 0


def test_multiline_expansions_over_file(monkeypatch):
    """Expand issues on each line when given multiple lines in a file"""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "geewhiz" and number == "101" and token is None:
            return {"html_url": "https://example.com/pulls/101", "title": "Foobar the Frobnitz"}
        elif group == "adamwolf" and repository == "geewhiz" and number == "102" and token is None:
            return {"html_url": "https://example.com/pulls/102", "title": "HOTFIX: fix the frobnitz!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("adamwolf/geewhiz#101\nhello world\nadamwolf/geewhiz#102")

        result = runner.invoke(cli, ["hello.txt"])
        assert result.output == (
            "[Foobar the Frobnitz #101](https://example.com/pulls/101)\n"
            "hello world\n"
            "[HOTFIX: fix the frobnitz! #102](https://example.com/pulls/102)"
        )
        assert result.exit_code == 0


def test_version():
    """--version prints the version"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.output == "cli, version 0.1.12\n"
    assert result.exit_code == 0


def test_help():
    """--help prints a helpful message"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert 'Turn references like "foo/bar#123" into Markdown links' in result.output


def test_cli_auth(monkeypatch):
    """Credentials can be passed on the command line"""

    def mockIssue(group, repository, number, token):
        if group == "foo" and repository == "privaterepo" and number == "555" and token == "password1":
            return {"html_url": "https://example.com/pulls/555", "title": "Sshhh!"}
        else:
            raise ValueError("Unexpected request")

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--github-token", "password1", "-"],
        input="foo/privaterepo#555",
    )
    assert result.output == "[Sshhh! #555](https://example.com/pulls/555)"
    assert result.exit_code == 0
