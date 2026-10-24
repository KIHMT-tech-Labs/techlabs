"""LeakCheck: a dependency-free, local-first secret scanner.

This is a best-effort safety net, not a replacement for a dedicated secret scanner.
It reports finding types and locations, never the matched secret value.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_FILE_BYTES = 1_000_000
SKIP_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "__pycache__",
    "node_modules", "dist", "build", ".next", ".tox",
}
PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Private key header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Credential assignment", re.compile(
        r"""(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b"""
        r"""\s*[:=]\s*["']?([A-Za-z0-9_./+=-]{12,})"""
    )),
)


def scan_file(path: Path) -> list[tuple[int, str]]:
    """Return (line number, finding type) pairs without returning secret text."""
    try:
        if path.is_symlink() or path.stat().st_size > MAX_FILE_BYTES:
            return []
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []

    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((line_number, label))
    return findings


def iter_files(root: Path, include_hidden: bool = False):
    if root.is_file():
        if include_hidden or not any(part.startswith(".") for part in root.parts):
            yield root
        return
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        yield path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan local files for common accidentally committed secrets."
    )
    parser.add_argument("path", nargs="?", default=".", help="File or directory to scan (default: current directory)")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and directories")
    args = parser.parse_args(argv)
    root = Path(args.path)

    if not root.exists():
        parser.error(f"path does not exist: {root}")
    if not root.is_file() and not root.is_dir():
        parser.error(f"path is not a regular file or directory: {root}")

    checked = 0
    total = 0
    for file_path in iter_files(root, args.include_hidden):
        checked += 1
        findings = scan_file(file_path)
        for line_number, label in findings:
            total += 1
            print(f"{file_path}:{line_number}: possible {label}")
    print(f"Scanned {checked} file(s); found {total} possible issue(s).")
    if total:
        print("Review findings manually. If a real secret was exposed, revoke/rotate it.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
