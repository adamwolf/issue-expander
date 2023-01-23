import re
import sys
from functools import partial

import click
import requests

# These regexes are really particular, at the moment..
regexes = [
    r"(?<![a-zA-Z0-9#])#(?P<number>\d+)(?![a-zA-Z0-9#])",  # like #123
    r"\bGH-(?P<number>\d+)",  # like GH-123
    r"(?P<group>[a-zA-Z0-9.-]+)/(?P<repository>[a-zA-Z0-9.-]+)#(?P<number>\d+)",  # like foo/bar#123
]


def getIssue(group: str, repository: str, number: int, username: [str], token: [str]) -> [dict]:
    # What to do with bad credentials?

    url = f"https://api.github.com/repos/{group}/{repository}/issues/{number}"
    if username and token:
        auth = (username, token)
    else:
        auth = None
    req = requests.get(url, auth=auth)
    if not req.ok:
        return None
    else:
        return req.json()


def substituteMatch(match, default_group, default_repository, username, token):
    if "group" in match.groupdict() and "repository" in match.groupdict():
        group = match.group("group")
        repository = match.group("repository")
    else:
        group = default_group
        repository = default_repository

    number = match.group("number")

    if group and repository:
        issue = getIssue(group, repository, number, username, token)
        if issue:
            html_url = issue["html_url"]
            title = issue["title"]
            # TODO do we need to escape [] or anything?
            return f"[{title} #{number}]({html_url})"
    # if we didn't find an issue, return the original text, so we don't change anything
    return match.group(0)


def expandRefsToMarkdown(
    text: str,
    username: object = None,
    token: object = None,
    default_group: object = None,
    default_repository: object = None,
) -> str:

    substituter = partial(
        substituteMatch,
        default_group=default_group,
        default_repository=default_repository,
        username=username,
        token=token,
    )
    # now substituter can be called with just one argument, the match

    out = text
    # make all the substitutions for this regex at one time,
    # then check that output string with the next regex

    for regex in regexes:
        out = re.sub(regex, substituter, out)
    return out


@click.command()
@click.option(
    "--default-source",
    metavar="USER/REPO",
    help='Use USER/REPO when not specified in issue reference. (Example: "adamwolf/issue-expander")',
)
@click.option(
    "-u",
    "--github-username",
    envvar="ISSUE_EXPANDER_GITHUB_USERNAME",
    metavar="USERNAME",
    help="GitHub username for looking up issue references. You can use the environment variable "
    "ISSUE_EXPANDER_GITHUB_USERNAME.",
)
@click.option(
    "-p",
    "--github-token",
    envvar="ISSUE_EXPANDER_GITHUB_TOKEN",
    metavar="TOKEN",
    help="GitHub token for looking up issue references. You may want to use the environment variable "
    "ISSUE_EXPANDER_GITHUB_TOKEN instead.",
)
@click.version_option()
@click.argument("input", metavar="FILE", type=click.File("r"))
def cli(input, github_username=None, github_token=None, default_source=None):
    """Turn references like "foo/bar#123" into Markdown links, like

    "[Prevent side fumbling #123](https://github.com/foo/bar/pull/123)"

    issue-expander works for references to issues and to pull requests.

    References are only expanded if they are found at GitHub.  To expand references from private
    repositories, you'll need to pass your GitHub username and token.  This can be done via
    environment variables or via command line options.

    To interpret references like `#1138` as `adamwolf/issue-expander#1138`,
    specify defaults using `--default-source`.
    """

    out = []

    default_group = None
    default_repository = None

    if default_source is not None:
        # default_group, default_repository = default_source.split("/")
        # get group/repository from default_source using a regex
        match = re.fullmatch(r"(?P<group>[a-zA-Z0-9.-]+)/(?P<repository>[a-zA-Z0-9.-]+)", default_source)
        if match:
            default_group = match.group("group")
            default_repository = match.group("repository")

        if not (default_group and default_repository):
            print("Error: default source must be in the format 'group/repository'", file=sys.stderr)
            sys.exit(1)

    for line in input:
        out = expandRefsToMarkdown(line, github_username, github_token, default_group, default_repository)
        print(out, end="")
