import responses

from issue_expander.issue_expander import expandRefsToMarkdown


@responses.activate
def test_issue_lookups_are_cached_in_a_line():
    """A line with multiple references to the same issue should only make one API call."""

    fake_issue = responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/999",
        json={
            "html_url": "https://example.com/issues/999",
            "title": "Cows don't meow",
        },
    )

    fake_pull = responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://example.com/pulls/101",
            "title": "Meow, meow, I'm a cow",
        },
    )

    expansion = expandRefsToMarkdown("adamwolf/geewhiz#101 adamwolf/geewhiz#999 adamwolf/geewhiz#101")
    expected = (
        "[Meow, meow, I'm a cow #101](https://example.com/pulls/101) "
        "[Cows don't meow #999](https://example.com/issues/999) "
        "[Meow, meow, I'm a cow #101](https://example.com/pulls/101)"
    )

    assert expansion == expected

    assert fake_issue.call_count == 1
    assert fake_pull.call_count == 1


@responses.activate
def test_issue_lookups_are_cached_across_lines():
    """A line with multiple references to the same issue should only make one API call."""

    fake_issue = responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/999",
        json={
            "html_url": "https://f.com/issues/999",
            "title": "Cows don't meow",
        },
    )

    fake_pull = responses.get(
        "https://api.github.com/repos/adamwolf/geewhiz/issues/101",
        json={
            "html_url": "https://f.com/pulls/101",
            "title": "Meow, meow, I'm a cow",
        },
    )

    expansion = expandRefsToMarkdown(
        "adamwolf/geewhiz#101 adamwolf/geewhiz#999\nadamwolf/geewhiz#101\nadamwolf/geewhiz#999 adamwolf/geewhiz#101"
    )
    lines = [
        "[Meow, meow, I'm a cow #101](https://f.com/pulls/101) [Cows don't meow #999](https://f.com/issues/999)",
        "[Meow, meow, I'm a cow #101](https://f.com/pulls/101)",
        "[Cows don't meow #999](https://f.com/issues/999) [Meow, meow, I'm a cow #101](https://f.com/pulls/101)",
    ]
    expected = "\n".join(lines)

    assert expansion == expected

    assert fake_issue.call_count == 1
    assert fake_pull.call_count == 1
