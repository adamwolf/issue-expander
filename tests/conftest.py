import pytest

from issue_expander.issue_expander import getIssue


@pytest.fixture(autouse=True)
def clear_issue_cache():
    getIssue.cache_clear()
