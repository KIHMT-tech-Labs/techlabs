# DevKit

A small, dependency-free Python command-line toolkit maintained by KIHMT Tech Labs. This is a code project, not a website.

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Run

From this directory, run commands like these:

    python devkit.py json-format '{"name":"KIHMT Tech Labs","active":true}'
    python devkit.py json-minify '{"name": "KIHMT Tech Labs", "active": true}'
    python devkit.py url-encode 'hello world & tea'
    python devkit.py url-decode 'hello%20world%20%26%20tea'
    python devkit.py base64-encode 'Hello, world!'
    python devkit.py base64-decode 'SGVsbG8sIHdvcmxkIQ=='
    python devkit.py timestamp-to-iso 0
    python devkit.py iso-to-timestamp '1970-01-01T00:00:00Z'

For HTML form-style URL encoding/decoding, add --form to the relevant URL command. JSON formatting supports --indent N.

## Run tests

From this directory:

    python -m unittest -v

## Notes

- Invalid JSON and invalid Base64 inputs return an error rather than silently producing output.
- ISO date/time input must include a timezone, such as Z or +05:30.
- Timestamp conversion uses Unix seconds and UTC ISO-8601 output.
- Do not put passwords, API keys, access tokens, or other secrets into command history or public issue reports.

## Project status

Initial version. Future additions should remain useful, tested, and focused on developer workflows.
