# git usage

See also my [system config](../System-Config/general.md).

I'm trying to keep this file here more about tips, tricks, and usage.

## Finding deleted files in the history (possibly from long ago)

Search the contents of all files that have ever existed in git for a string:

```bash
git log --summary -S<string> [<path/to/file>] [--since=2009.1.1] [--until=2010.1.1]
```
