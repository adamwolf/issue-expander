# Issue Expander

Use the GitHub API to turn issue references into Markdown links.

```

$ echo 'rust-lang/rust#106827' | issue-expander -
[Update LLVM to 15.0.7 #106827](https://github.com/rust-lang/rust/pull/106827)

$ echo '#106827' | issue-expander --default-source 'rust-lang/rust'
[Update LLVM to 15.0.7 #106827](https://github.com/rust-lang/rust/pull/106827)
```

This project is not yet stable in any way and makes absolutely no guarantees about behavior 
(between releases, or otherwise).

## Usage

```
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
Usage: issue-expander [OPTIONS] INPUT

  Use the GitHub API to turn issue references, like "rust-lang/rust#106827",
  into Markdown links, like

  "[Update LLVM to 15.0.7 #106827](https://github.com/rust-
  lang/rust/pull/106827)"

Options:
  --default-source USER/REPO  Use default when not specified in the issue
                              reference, formatted like '"adamwolf/issue-
                              expander".'
  -u, --github-username TEXT  GitHub username for looking up issue references.
                              You can use the environment variable
                              ISSUE_EXPANDER_GITHUB_USERNAME.
  -p, --github-token TEXT     GitHub token for looking up issue references. You
                              may want to use the environment variable
                              ISSUE_EXPANDER_GITHUB_TOKEN instead.
  --version                   Show the version and exit.
  --help                      Show this message and exit.

```
<!-- [[[end]]] -->
```
