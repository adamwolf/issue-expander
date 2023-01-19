import responses
from click.testing import CliRunner

from issue_expander.issue_expander import cli

# mock out the requests.get() call


@responses.activate
def test_file():
    """Test that the CLI works with a file"""
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
    """Test that we read from stdin if given - as the input file"""
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
def test_default_source():
    """Test that we can use a default group/repository"""
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
    """Test that we don't use a default group/repository if one is specified in the input"""
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


# TODO test username implies token
# TODO test token implies username

# @responses.activate
# def test_two_expansions_in_one_line(): # TODO FIXME
#     """Test that we can expand multiple issues in one line"""
#     responses.get("https://api.github.com/repos/adamwolf/geewhiz/issues/101",
#     json={"html_url": "https://example.com/pulls/101", "title": "Foobar the Frobnitz"})
#     responses.get("https://api.github.com/repos/adamwolf/geewhiz/issues/102",
#     json={"html_url": "https://example.com/pulls/102", "title": "HOTFIX: fix the frobnitz!"})
#
#     runner = CliRunner()
#     result = runner.invoke(cli, ['-'], input='adamwolf/geewhiz#101 adamwolf/geewhiz#102')
#     assert False


@responses.activate
def test_multiline_expansions_over_stdin():
    """Test that we can expand issues on multiple lines"""
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
    """Test that we can expand issues on multiple lines"""
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


# def test_version():
#     """Test that we can print the version"""
#     runner = CliRunner()
#     result = runner.invoke(cli, ["--version"])
#     assert result.output == "geewhiz version "
#     assert result.exit_code == 0
