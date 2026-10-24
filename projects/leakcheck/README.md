# LeakCheck

A small, dependency-free Python utility that checks local project files for common signs of accidentally committed credentials.

## Why use it?

Secrets can accidentally end up in source code, configuration files, or copied logs. LeakCheck provides a quick local pre-flight check before you commit or push.

## Requirements

- Python 3.10+
- No third-party packages

## Usage

From the repository root:

```bash
python projects/leakcheck/leakcheck.py .
```

Scan a single file:

```bash
python projects/leakcheck/leakcheck.py .env.example
```

Include hidden files and directories:

```bash
python projects/leakcheck/leakcheck.py . --include-hidden
```

The command returns exit code `1` when possible findings are detected, and `0` when none are detected. It prints the file, line number, and finding category—not the matched credential itself.

## Run tests

```bash
python -m unittest discover -s projects/leakcheck -p 'test_*.py' -v
```

## Limitations

- This is a best-effort scanner, not a guarantee that a repository is secret-free.
- Pattern matching can produce false positives and miss unfamiliar secret formats.
- Hidden files are skipped by default; use `--include-hidden` to scan them.
- Files over 1 MB, binary/non-UTF-8 files, symlinks, and common generated directories are skipped.
- Review results manually. If a real credential was exposed, revoke or rotate it immediately; deleting a line from the latest version does not invalidate a leaked credential.

## License

MIT. See the repository's root license file, if present, for the project-wide licensing terms.
