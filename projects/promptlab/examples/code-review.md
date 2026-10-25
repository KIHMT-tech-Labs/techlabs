# Code review prompt

You are reviewing a change written in {{language}}.

Review the change below for correctness, edge cases, readability, and maintainability. Prioritize concrete issues over style preferences. Do not invent problems that are not supported by the code.

## Change

```{{language}}
{{diff}}
```

## Response format

For each finding, include:
- Severity: blocker, high, medium, or low
- Location: the relevant function or line when available
- Problem: what can go wrong
- Suggested fix: a practical improvement

If you find no actionable issues, say so and briefly mention what you checked.
