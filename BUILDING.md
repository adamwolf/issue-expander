# Building

If you'd like to run issue-expander, you probably want to use the installation instructions in the [README](README.md).

However, we do have PyOxidizer set up to make a binary that includes Python and the dependencies in one file.

## PyOxidizer

[PyOxidizer](https://github.com/indygreg/PyOxidizer) is a pretty slick project.  It can often make a relatively portable binary that has Python and all the dependencies included.

(I am not an expert on PyOxidizer.  Please let me know if you want to help with PyOxidizer on this project!)

## Building

Install PyOxidizer and run `pyoxidizer build` in the root of the repository.

One way this can be done is like this:

```
pip install pyoxidizer
pyoxidizer build
```

The resulting output will be in the `build/` directory.

You can make binaries with the debug symbols stripped by adding `--release` to the build command line.

## Distribution

PyOxidizer has documentation on [distributing applications built with PyOxidizer](https://gregoryszorc.com/docs/pyoxidizer/main/pyoxidizer_distributing.html).

If you work through this for issue-expander, please let me know.

### Licensing

I am not a legal expert.  I am not a lawyer.

PyOxidizer has some documentation on [licensing considerations](https://gregoryszorc.com/docs/pyoxidizer/main/pyoxidizer_packaging_licensing.html#licensing-considerations).

I think it is true that the licenses of many Python libraries treat distributing binaries of Python programs differently than distributing source code, and they may treat distributing binaries that include the library differently than distributing binaries that do not include the library.

PyOxidizer looks for licensing in the metadata of the components used and prints a summary during the build.
