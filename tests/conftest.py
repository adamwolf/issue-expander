import pytest

from issue_expander.issue_expander import getIssue


@pytest.fixture(autouse=True)
def smtp_connection():
    getIssue.cache_clear()
