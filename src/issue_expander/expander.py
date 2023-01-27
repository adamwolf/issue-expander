import json
import re
import ssl
import sys
from functools import lru_cache, partial
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import certifi
import click

# These regexes are really particular, at the moment...
# When adding regexes, take care to only match if you should--this may mean negative look-ahead and -behind assertions
# and name the group number, owner, and repository, but append _ and a unique suffix.

# Python's re module doesn't support regexes containing multiple named groups with the same name.

# These regexes are later combined into a megaregex.
named_regexes = [
    # like https://github.com/foo/bar/issues/123
    r"https://github.com/(?P<owner_x>[a-zA-Z0-9.-]+)/(?P<repository_x>[a-zA-Z0-9.-]+)/(issues|pull)/(?P<number_x>\d+)",
    r"(?<![a-zA-Z0-9#-])#(?P<number_y>\d+)(?![a-zA-Z0-9#])",  # like #123
    r"\bGH-(?P<number_z>\d+)",  # like GH-123
    r"(?P<owner_n>[a-zA-Z0-9.-]+)/(?P<repository_n>[a-zA-Z0-9.-]+)#(?P<number_n>\d+)",  # like foo/bar#123
]

megaregex = re.compile("|".join(named_regexes))


@lru_cache()
def getIssue(owner: str, repository: str, number: int, token: [str]) -> [dict]:
    # What to do with bad credentials?

    url = f"https://api.github.com/repos/{owner}/{repository}/issues/{number}"

    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer: {token}"

    request = Request(url, headers=headers)

    certifi_context = ssl.create_default_context(cafile=certifi.where())

    try:
        with urlopen(request, context=certifi_context) as response:
            j = json.load(response)
            return j
    except HTTPError as e:
        if e.code == 403:  # "rate limit exceeded"
            message = "Unable to look up issue due to rate limit error."
            if not token:
                message += " Try providing a token with --token."
            print(message, file=sys.stderr)
    except json.JSONDecodeError:
        print(f"Unable to parse response from {url}", file=sys.stderr)
        return None


def substituteMatch(match, default_owner, default_repository, token):
    owner = None
    repository = None
    number = None

    for name, value in match.groupdict().items():
        if name.startswith("number_") and value is not None:
            number = value
        elif name.startswith("owner_") and value is not None:
            owner = value
        elif name.startswith("repository_") and value is not None:
            repository = value

    if not (owner and repository):
        owner = default_owner
        repository = default_repository

    if owner and repository:
        issue = getIssue(owner, repository, number, token)
        if issue:
            html_url = issue["html_url"]
            title = issue["title"]
            # TODO do we need to escape [] or anything?
            return f"[{title} #{number}]({html_url})"
    # if we didn't find an issue, return the original text, so we don't change anything
    return match.group(0)


def expandRefsToMarkdown(
    text: str,
    token: object = None,
    default_owner: object = None,
    default_repository: object = None,
) -> str:
    substituter = partial(
        substituteMatch,
        default_owner=default_owner,
        default_repository=default_repository,
        token=token,
    )
    # now substituter can be called with just one argument, the match

    out = text
    # make all the substitutions for this regex at one time,
    # then check that output string with the next regex

    out = re.sub(megaregex, substituter, out)
    return out


@click.command()
@click.option(
    "--default-source",
    metavar="USER/REPO",
    help='Use USER/REPO when not specified in issue reference. (Example: "adamwolf/issue-expander")',
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
def cli(input, github_token=None, default_source=None):
    """Turn references like "foo/bar#123" into Markdown links, like

    "[Prevent side fumbling #123](https://github.com/foo/bar/pull/123)"

    issue-expander works for references to issues and to pull requests.

    References are only expanded if they are found at GitHub.  To expand references from private
    repositories, you'll need to pass your GitHub token.  This can be done via environment
    variables or via command line options.

    To interpret references like `#1138` as `adamwolf/issue-expander#1138`,
    specify defaults using `--default-source`.
    """

    out = []

    default_owner = None
    default_repository = None

    if default_source is not None:
        # get owner/repository from default_source using a regex
        match = re.fullmatch(r"(?P<owner>[a-zA-Z0-9.-]+)/(?P<repository>[a-zA-Z0-9.-]+)", default_source)
        if match:
            default_owner = match.group("owner")
            default_repository = match.group("repository")

        if not (default_owner and default_repository):
            print("Error: default source must be in the format 'owner/repository'", file=sys.stderr)
            sys.exit(1)

    for line in input:
        out = expandRefsToMarkdown(line, github_token, default_owner, default_repository)
        print(out, end="")
