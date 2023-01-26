# issue-expander

*Expand GitHub issue references into Markdown links*

[![PyPI](https://img.shields.io/pypi/v/issue-expander?color=green&logo=python&logoColor=white)](https://pypi.org/project/issue-expander/)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/adamwolf/4537e853375d0289662b6c7741571cb0/raw/covbadge.json)

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
from issue_expander import expander
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(expander.cli, ["--help"])
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
  references from private repositories, you'll need to pass your GitHub token.
  This can be done via environment variables or via command line options.

  To interpret references like `#1138` as `adamwolf/issue-expander#1138`,
  specify defaults using `--default-source`.

Options:
  --default-source USER/REPO  Use USER/REPO when not specified in issue
                              reference. (Example: "adamwolf/issue-expander")
  -p, --github-token TOKEN    GitHub token for looking up issue references. You
                              may want to use the environment variable
                              ISSUE_EXPANDER_GITHUB_TOKEN instead.
  --version                   Show the version and exit.
  --help                      Show this message and exit.

```
<!-- [[[end]]] -->

## Installation

If you use Homebrew, you can install issue-expander like this:
<!-- [[[cog
import cog
with open("_docs/install-via-homebrew.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
brew tap adamwolf/issue-expander
brew install issue-expander
```
<!-- [[[end]]] -->

Otherwise, I recommend installing with [pipx](https://pypa.github.io/pipx/). Once you've got pipx installed, you can install issue-expander like this:

<!-- [[[cog
import cog
with open("_docs/install-via-pipx.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
pipx install issue-expander
```
<!-- [[[end]]] -->

and pipx installs issue-expander into its own little area, just for you, where you don't have to worry about it messing with any system-wide or even user-wide Python dependencies.

If you want to generate a binary that can run issue-expander without needing Python to be installed, see [BUILDING.md](BUILDING.md).

If you want to do something different, issue-expander is available on PyPI. Go hogwild.

## Development

There are a lot of ways to set up a development environment for a Python application.  This is one of them.

Before you follow these steps, make sure Python 3 is installed.

1. Clone the issue-expander repository.
<!-- [[[cog
import cog
with open("_docs/devclone.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
git clone https://github.com/adamwolf/issue-expander.git
```
<!-- [[[end]]] -->

2. Create a virtual environment and activate it.

<!-- [[[cog
import cog
with open("_docs/devvenv.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
cd issue-expander
python3 -m venv venv
source venv/bin/activate
```
<!-- [[[end]]] -->

3. Install the package in editable mode (with development extras).
<!-- [[[cog
import cog
with open("_docs/devinstall.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
pip install -e .[dev]
```
<!-- [[[end]]] -->

4. Make sure you can run the tests.
<!-- [[[cog
import cog
with open("_docs/devtest.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
pytest
```
<!-- [[[end]]] -->

5. Make sure you can run the linter.
<!-- [[[cog
import cog
with open("_docs/devlint.txt") as f:
    cog.out("```\n")
    for line in f:
        cog.out(line)
    cog.out("```\n")
]]] -->
```
pre-commit run --all-files
```
<!-- [[[end]]] -->

At this point, you should be able to make changes to the code.

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
