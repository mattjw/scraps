### Launching a Crawler Process

See `starter.sh`, which launches the example `demo.py` script.

#### `stdbuf` on OS X

Two approaches, both use homebrew:

* Install homebrew's `coreutils`. (Switches toolchain to GNU, which may cause issues for any OS X scripts that depend on the vanilla OS X toolchain.) This will include `stdbuf`.
* Install `stdbuf`-specifically, via a third-party homebrew. See below.

```
brew tap paulp/extras
brew install paulp/extras/stdbuf
```