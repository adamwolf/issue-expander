import pytest

from issue_expander.expander import getIssue


@pytest.fixture(autouse=True)
def clear_issue_cache():
    getIssue.cache_clear()
