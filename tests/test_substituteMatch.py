import re

import responses

from issue_expander.issue_expander import substituteMatch


@responses.activate
def test_substituteMatch_with_group_but_no_repo():
    """If a group is specified but not a repo, use the default repo"""

    # make a match without a repository group, and don't give it a default repository
    match = re.match(r"(?P<group>adamwolf)/geewhiz#(?P<number>\d+)", "adamwolf/geewhiz#101")
    assert match
    assert match.group("group") == "adamwolf"
    assert match.group("number") == "101"

    # let's make sure we didn't call out at all
    rsp = responses.get(re.compile("http.*"))

    assert substituteMatch(match, "defaultgroup", None, None, None) == ("adamwolf/geewhiz#101")

    assert rsp.call_count == 0
