# Releases

## Preparation

Bump the version in `pyproject.toml` by removing the `.devx`.  Update the test!

Use `scriv collect` to create an initial changelog.  Review it.

Make a branch. Make a commit with the `changelog.d/` removals, the `CHANGELOG.md` changes,
the `pyproject.toml` version change...

After the PR is merged, pull, and make a tag with `git tag vx.y.z`.

Push the tag with `git push --tags`.

## Build PyPI packages and wheels

(It would be great to build more wheels here!)

```
pip install build twine
rm -rf build dist
python -m build .
twine check dist/*`
```

Do whatever testing you need.  If you did anything weird or to metadata, you can push to Test PyPI with `twine upload -r test dist/*`, otherwise:

`twine upload -r issue-expander dist/*`


## Homebrew tap

Update homebrew-issue-expander with `brew bump-version-pr issue-expander --version x.y.z`

Once the pull request passes the builds, add a `pr-pull` tag to continue the automation.

## Get ready for more development

Make a new branch.  Increment the version number and add a `.dev0`.  (Update the test!) Make a pull request and merge it.

## GitHub release
scriv will create a GitHub release based on the latest tag and entry in the CHANGELOG.md file.

```
scriv github-release --dry-run
export GITHUB_TOKEN=password1
scriv github-release
```
