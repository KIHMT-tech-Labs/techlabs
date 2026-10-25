# PromptLab

A small, local-first toolkit for developers who work with AI prompts. Save reusable prompts as plain Markdown, check templates for common placeholder mistakes, and render a prompt with supplied values — without an API key or external service.

PromptLab is intentionally provider-neutral: it helps with the prompt workflow, not with calling a particular model.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Quick start

From the repository root:

```bash
python projects/promptlab/promptlab.py list
python projects/promptlab/promptlab.py check projects/promptlab/examples/code-review.md
python projects/promptlab/promptlab.py render projects/promptlab/examples/code-review.md --var language=Python --var diff="def add(a, b): return a + b"
```

To see every command and option:

```bash
python projects/promptlab/promptlab.py --help
python projects/promptlab/promptlab.py render --help
```

## Prompt format

Use named placeholders in double braces, such as `{{language}}` and `{{diff}}`. Keep one prompt per Markdown file. An example is included in `examples/code-review.md`.

- `list [directory]` lists Markdown prompt files (defaults to the bundled examples).
- `check FILE` reports placeholders and basic template issues.
- `render FILE --var name=value` substitutes provided values and prints the result.
- `init PATH` creates a starter prompt file without overwriting an existing file.

## Why local-first?

- No model provider is required.
- No network requests are made.
- Prompt content stays in your local files and terminal.
- Templates can be reviewed and version-controlled like ordinary source code.

## Tests

```bash
python -m unittest discover -s projects/promptlab -p 'test_*.py' -v
```

## Scope and limitations

PromptLab performs simple text-template substitution, not model inference. It does not execute prompt content. Placeholder names must use letters, digits, or underscores and begin with a letter or underscore. Values are plain text; this tool does not attempt to escape content for a particular model or downstream format.

## Contributing

Bug reports, examples, small improvements, and tests are welcome. Please read the repository's contribution guidance before opening a pull request.

## License

See the repository root for the project's license.
