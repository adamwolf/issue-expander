import re
import sys

import click
import requests

# These regexes are really particular, at the moment..
regexes = [
    r"(?<![a-zA-Z0-9#])#(?P<number>\d+)(?![a-zA-Z0-9#])",  # like #123 #
    r"(?P<group>[a-zA-Z0-9.-]+)/(?P<repository>[a-zA-Z0-9.-]+)#(?P<number>\d+)",  # like foo/bar#123
]


def getIssue(group: str, repository: str, number: object, username: object, token: object) -> [dict]:
    if not group or not repository or not number:
        return None

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


def expandRefsToMarkdown(
    text: str,
    username: object = None,
    token: object = None,
    default_group: object = None,
    default_repository: object = None,
) -> str:
    out = text

    for regex in regexes:
        for match in re.finditer(regex, out):
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
                    # Replace just the match with the markdown expansion
                    out = out[: match.start()] + f"[{title} #{number}]({html_url})" + out[match.end() :]
    return out


def validate_token(ctx, param, value):
    if value and not ctx.params["github_username"]:
        raise click.UsageError("Cannot pass --github-token without --github-username")


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
    callback=validate_token,
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

    if default_source:
        default_good = True
        try:
            default_group, default_repository = default_source.split("/")
        except ValueError:
            default_good = False
        else:
            if not default_group or not default_repository:
                default_good = False

        if not default_good:
            print(
                "Error: default source must be in the format 'group/repository'",
                file=sys.stderr,
            )
            sys.exit(1)

    for line in input:
        out = expandRefsToMarkdown(line, github_username, github_token, default_group, default_repository)
        print(out, end="")


if __name__ == "__main__":
    cli()
