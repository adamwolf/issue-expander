import re

import issue_expander
from issue_expander.expander import substituteMatch


def test_substituteMatch_with_group_but_no_repo(monkeypatch):
    """If a group is specified but not a repo, use the default repo"""

    def noRequests(*args, **kwargs):
        raise AssertionError("shouldn't have made a request")

    monkeypatch.setattr("urllib.request.urlopen", noRequests)

    # make a match without a repository group, and don't give it a default repository
    match = re.match(r"(?P<group>adamwolf)/geewhiz#(?P<number>\d+)", "adamwolf/geewhiz#101")
    assert match
    assert match.group("group") == "adamwolf"
    assert match.group("number") == "101"

    assert substituteMatch(match, "defaultgroup", None, None, None) == ("adamwolf/geewhiz#101")


def test_substituteMatch_with_no_issue_found_online(monkeypatch):
    """If we try to look up an issue, and it can't be found, don't expand it."""

    def all_404s(*args, **kwargs):
        return None

    monkeypatch.setattr(issue_expander.expander, "getIssue", all_404s)

    match = re.match(r"\bGH-(?P<number>\d+)", "GH-101")
    assert match

    assert substituteMatch(match, "defaultgroup", "adamwolf", "bogus", None) == ("GH-101")
