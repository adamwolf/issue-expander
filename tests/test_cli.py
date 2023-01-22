"""
Use the CLI directly for some high-level integration tests.
"""

import responses
from click.testing import CliRunner

from issue_expander.issue_expander import cli

# TODO test username implies token
# TODO test token implies username


@responses.activate
def test_file():
    """Use a file as input."""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/106970",
            "title": "Foobar the Frobnitz",
        },
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("adamwolf/geewhiz#101")

        result = runner.invoke(cli, ["hello.txt"])
        assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
        assert result.exit_code == 0


@responses.activate
def test_stdin():
    """Read input from stdin if given - as the input file."""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/106970",
            "title": "Foobar the Frobnitz",
        },
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101")
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0

@responses.activate
def test_404s_dont_expand():
    """If something looks like an issue reference, but GitHub 404s, don't expand it."""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        status = 404
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101")
    assert result.output == "adamwolf/geewhiz#101"
    assert result.exit_code == 0

@responses.activate
def test_default_source():
    """Use a default group/repository when specified as an option."""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/106970",
            "title": "Foobar the Frobnitz",
        },
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["--default-source", "adamwolf/geewhiz", "-"], input="#101")
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0


@responses.activate
def test_default_source_but_not_needed():
    """Don't override a specified group/repository even if a default is specified"""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/106970",
            "title": "Foobar the Frobnitz",
        },
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--default-source", "adamwolf/defaultdefault", "-"],
        input="adamwolf/geewhiz#101",
    )
    assert result.output == "[Foobar the Frobnitz #101](https://example.com/pulls/106970)"
    assert result.exit_code == 0


@responses.activate
def test_two_expansions_in_one_line():
    """Test that we can expand multiple issues in one line"""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={"html_url": "https://example.com/pulls/101", "title": "Foobar the Frobnitz"},
    )
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/102",
        json={"html_url": "https://example.com/pulls/102", "title": "HOTFIX: fix the frobnitz!"},
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101 adamwolf/geewhiz#102")
    assert result.output == (
        "[Foobar the Frobnitz #101](https://example.com/pulls/101) [HOTFIX: fix the frobnitz! #102](https://example.com/pulls/102)"
    )


@responses.activate
def test_multiline_expansions_over_stdin():
    """Expand issues on each line when given multiple lines through stdin"""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/101",
            "title": "Foobar the Frobnitz",
        },
    )
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/102",
        json={
            "html_url": "https://example.com/pulls/102",
            "title": "HOTFIX: fix the frobnitz!",
        },
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["-"], input="adamwolf/geewhiz#101\nhello world\nadamwolf/geewhiz#102")
    assert result.output == (
        "[Foobar the Frobnitz #101](https://example.com/pulls/101)\n"
        "hello world\n"
        "[HOTFIX: fix the frobnitz! #102](https://example.com/pulls/102)"
    )
    assert result.exit_code == 0


@responses.activate
def test_multiline_expansions_over_file():
    """Expand issues on each line when given multiple lines in a file"""
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/101",
            "title": "Foobar the Frobnitz",
        },
    )
    responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/102",
        json={
            "html_url": "https://example.com/pulls/102",
            "title": "HOTFIX: fix the frobnitz!",
        },
    )

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
    """Test that we can print the version"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.output == "cli, version 0.1.10.dev0\n"
    assert result.exit_code == 0


def test_help():
    """Test that we can print the help"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert 'Turn references like "foo/bar#123" into Markdown links' in result.output
