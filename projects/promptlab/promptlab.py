"""PromptLab: simple local tools for reusable AI prompt templates."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")
ANY_PLACEHOLDER_RE = re.compile(r"{{(.*?)}}")
DEFAULT_EXAMPLES = Path(__file__).parent / "examples"


def read_prompt(path: Path) -> str:
    """Read a UTF-8 prompt file, raising a helpful error on failure."""
    try:
        if not path.is_file():
            raise ValueError(f"not a file: {path}")
        return path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        raise ValueError(f"prompt is not valid UTF-8: {path}") from exc
    except OSError as exc:
        raise ValueError(f"could not read {path}: {exc}") from exc


def placeholders(template: str) -> list[str]:
    """Return unique valid placeholder names in first-seen order."""
    return list(dict.fromkeys(match.group(1) for match in PLACEHOLDER_RE.finditer(template)))


def inspect_template(template: str) -> list[str]:
    """Return template issues without modifying the source."""
    issues: list[str] = []
    valid_spans = {m.span() for m in PLACEHOLDER_RE.finditer(template)}
    for match in ANY_PLACEHOLDER_RE.finditer(template):
        if match.span() not in valid_spans:
            issues.append(f"invalid placeholder syntax: {{{{{match.group(1)}}}}}")
    return issues


def render_template(template: str, values: dict[str, str]) -> str:
    """Substitute known placeholders and reject missing or unused values."""
    issues = inspect_template(template)
    if issues:
        raise ValueError("; ".join(issues))

    required = set(placeholders(template))
    supplied = set(values)
    missing = sorted(required - supplied)
    unused = sorted(supplied - required)
    if missing:
        raise ValueError("missing value(s): " + ", ".join(missing))
    if unused:
        raise ValueError("unused value(s): " + ", ".join(unused))
    return PLACEHOLDER_RE.sub(lambda m: values[m.group(1)], template)


def list_prompts(directory: Path) -> list[Path]:
    """List Markdown files in a directory, in a stable order."""
    if not directory.is_dir():
        raise ValueError(f"not a directory: {directory}")
    return sorted((p for p in directory.rglob("*.md") if p.is_file()), key=lambda p: str(p).lower())


def command_list(args: argparse.Namespace) -> int:
    directory = Path(args.directory) if args.directory else DEFAULT_EXAMPLES
    files = list_prompts(directory)
    if not files:
        print(f"No Markdown prompts found in {directory}")
        return 0
    for path in files:
        print(path)
    print(f"{len(files)} prompt(s)")
    return 0


def command_check(args: argparse.Namespace) -> int:
    path = Path(args.file)
    template = read_prompt(path)
    issues = inspect_template(template)
    names = placeholders(template)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1
    print(f"OK: {path}")
    print("Placeholders: " + (", ".join(names) if names else "(none)"))
    return 0


def parse_var(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(f"expected NAME=VALUE, got: {raw}")
    name, value = raw.split("=", 1)
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"invalid variable name: {name}")
    return name, value


def command_render(args: argparse.Namespace) -> int:
    path = Path(args.file)
    template = read_prompt(path)
    values: dict[str, str] = {}
    for raw in args.var:
        name, value = parse_var(raw)
        if name in values:
            raise ValueError(f"variable supplied more than once: {name}")
        values[name] = value
    print(render_template(template, values), end="")
    if not template.endswith("\n"):
        print()
    return 0


def command_init(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if path.exists():
        raise ValueError(f"refusing to overwrite existing path: {path}")
    content = (
        "# New prompt\n\n"
        "Describe the task and any constraints clearly.\n\n"
        "## Context\n\n{{context}}\n\n"
        "## Expected output\n\n{{expected_output}}\n"
    )
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"could not create prompt file: {exc}") from exc
    print(f"Created {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PromptLab: local tools for reusable AI prompt templates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list Markdown prompt files")
    list_parser.add_argument("directory", nargs="?", help="directory to search (default: bundled examples)")
    list_parser.set_defaults(func=command_list)

    check_parser = subparsers.add_parser("check", help="check a prompt template")
    check_parser.add_argument("file", help="path to a Markdown prompt file")
    check_parser.set_defaults(func=command_check)

    render_parser = subparsers.add_parser("render", help="render a template with NAME=VALUE arguments")
    render_parser.add_argument("file", help="path to a Markdown prompt file")
    render_parser.add_argument("--var", action="append", default=[], metavar="NAME=VALUE",
                               help="set a placeholder value; may be repeated")
    render_parser.set_defaults(func=command_render)

    init_parser = subparsers.add_parser("init", help="create a starter prompt file")
    init_parser.add_argument("path", help="new Markdown file path")
    init_parser.set_defaults(func=command_init)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
