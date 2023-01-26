# v0.1.12 -- 2023-01-25

## Removed

- Removed dependency on requests, to make it easiedr to package with PyOxidizer. (#37)
- Removed username parameter--we've never used it. (#44)

## Added

- Added a __main__ handler, so `python -m issue_expander` runs the CLI. (#42)
- Added PyOxidizer build configuration and documentation. (#35)
- Added changelog.
- Added pull request template.
- Added developer instructions with automatic testing.
- Added installation instructions with automated testing.
- Added documentation on contributing.
- Added security policy.
- Added web request cache. (#23)
- Added expansion of basic GitHub URL issue references.
- Added a lot of tests.

## Fixed

- Fixed bug with double expansion of URLs.
