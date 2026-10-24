"""Small, dependency-free command-line utilities for developers."""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import math
from datetime import datetime, timezone
from urllib.parse import quote, unquote, quote_plus, unquote_plus


def format_json(value: str, *, indent: int = 2) -> str:
    """Validate JSON and return a readable representation."""
    return json.dumps(json.loads(value), indent=indent, ensure_ascii=False)


def minify_json(value: str) -> str:
    """Validate JSON and remove unnecessary whitespace."""
    return json.dumps(json.loads(value), separators=(",", ":"), ensure_ascii=False)


def url_encode(value: str, *, form: bool = False) -> str:
    """Percent-encode text; optionally use HTML form encoding."""
    return quote_plus(value) if form else quote(value, safe="")


def url_decode(value: str, *, form: bool = False) -> str:
    """Decode percent-encoded text."""
    return unquote_plus(value) if form else unquote(value)


def base64_encode(value: str) -> str:
    """Encode UTF-8 text as Base64."""
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def base64_decode(value: str) -> str:
    """Decode Base64 text as UTF-8, rejecting malformed input."""
    try:
        return base64.b64decode(value, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Input must be valid Base64 containing UTF-8 text.") from exc


def timestamp_to_iso(value: str) -> str:
    """Convert Unix seconds to UTC ISO-8601."""
    try:
        seconds = float(value)
        if not math.isfinite(seconds):
            raise ValueError
        result = datetime.fromtimestamp(seconds, tz=timezone.utc)
    except (ValueError, OverflowError, OSError) as exc:
        raise ValueError("Provide a valid Unix timestamp in seconds.") from exc
    return result.isoformat().replace("+00:00", "Z")


def iso_to_timestamp(value: str) -> str:
    """Convert a timezone-aware ISO-8601 date/time to Unix seconds."""
    try:
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        result = datetime.fromisoformat(normalized)
        if result.tzinfo is None:
            raise ValueError("Timezone is required; use Z or an explicit UTC offset.")
        return str(result.timestamp())
    except ValueError as exc:
        raise ValueError(
            "Provide an ISO-8601 date/time with timezone, e.g. 2026-01-01T12:00:00Z."
        ) from exc


COMMANDS = {
    "json-format": format_json,
    "json-minify": minify_json,
    "url-encode": url_encode,
    "url-decode": url_decode,
    "base64-encode": base64_encode,
    "base64-decode": base64_decode,
    "timestamp-to-iso": timestamp_to_iso,
    "iso-to-timestamp": iso_to_timestamp,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="KIHMT Tech Labs DevKit: small developer utilities."
    )
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("value", help="Input value; for JSON, pass the complete JSON text.")
    parser.add_argument("--indent", type=int, default=2,
                        help="Indent width for json-format (default: 2).")
    parser.add_argument("--form", action="store_true",
                        help="Use form encoding for URL conversion.")
    args = parser.parse_args()

    if args.indent < 0:
        parser.error("--indent must be zero or greater")

    try:
        if args.command == "json-format":
            output = format_json(args.value, indent=args.indent)
        elif args.command == "url-encode":
            output = url_encode(args.value, form=args.form)
        elif args.command == "url-decode":
            output = url_decode(args.value, form=args.form)
        else:
            output = COMMANDS[args.command](args.value)
    except (ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"error: {exc}\n")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
