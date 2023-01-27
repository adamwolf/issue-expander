import issue_expander
from issue_expander.expander import expandRefsToMarkdown


def test_gh_url_expansion(monkeypatch):
    """Issue references should only expand once."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "faux-expander" and number == "23" and token is None:
            return {
                "html_url": "https://github.com/adamwolf/faux-expander/issues/23",
                "title": "Do not double expand references like adamwolf/faux-expander#100",
            }

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown("adamwolf/faux-expander#23")
    assert (
        expansion == "[Do not double expand references like adamwolf/faux-expander#100 #23]"
        "(https://github.com/adamwolf/faux-expander/issues/23)"
    )


def test_double_url_expansion(monkeypatch):
    """Issue references should only expand once."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "faux-expander" and number == "23" and token is None:
            return {
                "html_url": "https://github.com/adamwolf/faux-expander/issues/23",
                "title": "Not https://github.com/adamwolf/faux-expander/issues/23 "
                "nor https://github.com/adamwolf/faux-expander/issues/24",
            }

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown("adamwolf/faux-expander#23")
    assert (
        expansion == "[Not https://github.com/adamwolf/faux-expander/issues/23 nor "
        "https://github.com/adamwolf/faux-expander/issues/24 "
        "#23](https://github.com/adamwolf/faux-expander/issues/23)"
    )


def test_double_gh_expansion(monkeypatch):
    """Issue references should only expand once."""

    def mockIssue(group, repository, number, token):
        if group == "adamwolf" and repository == "faux-expander" and number == "23" and token is None:
            return {
                "html_url": "https://github.com/adamwolf/faux-expander/issues/23",
                "title": "Refix GH-22",
            }

    monkeypatch.setattr(issue_expander.expander, "getIssue", mockIssue)

    expansion = expandRefsToMarkdown("GH-23", default_group="adamwolf", default_repository="faux-expander")
    assert expansion == "[Refix GH-22 #23](https://github.com/adamwolf/faux-expander/issues/23)"
