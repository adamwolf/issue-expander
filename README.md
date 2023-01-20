# issue-expander

Expand GitHub issue references into Markdown links.

```
$ echo 'rust-lang/rust#106827' | issue-expander -
[Update LLVM to 15.0.7 #106827](https://github.com/rust-lang/rust/pull/106827)

$ echo '#106827' | issue-expander --default-source 'rust-lang/rust'
[Update LLVM to 15.0.7 #106827](https://github.com/rust-lang/rust/pull/106827)
```

This project is not yet stable in any way and makes absolutely no guarantees about behavior
(between releases, or otherwise).

## Usage


<!-- [[[cog
import cog
from issue_expander import issue_expander
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(issue_expander.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: issue-expander")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: issue-expander [OPTIONS] FILE

  Turn references like "foo/bar#123" into Markdown links, like

  "[Prevent side fumbling #123](https://github.com/foo/bar/pull/123)"

  issue-expander works for references to issues and to pull requests.

  References are only expanded if they are found at GitHub.  To expand
  references from private repositories, you'll need to pass your GitHub username
  and token.  This can be done via environment variables or via command line
  options.

  To interpret references like `#1138` as `adamwolf/issue-expander#1138`,
  specify defaults using `--default-source`.

Options:
  --default-source USER/REPO      Use USER/REPO when not specified in issue
                                  reference. (Example: "adamwolf/issue-
                                  expander")
  -u, --github-username USERNAME  GitHub username for looking up issue
                                  references. You can use the environment
                                  variable ISSUE_EXPANDER_GITHUB_USERNAME.
  -p, --github-token TOKEN        GitHub token for looking up issue references.
                                  You may want to use the environment variable
                                  ISSUE_EXPANDER_GITHUB_TOKEN instead.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

```
<!-- [[[end]]] -->
