import tempfile
import unittest
from pathlib import Path

from promptlab import (
    inspect_template,
    list_prompts,
    parse_var,
    placeholders,
    render_template,
)


class PromptLabTests(unittest.TestCase):
    def test_placeholders_are_unique_and_ordered(self):
        self.assertEqual(placeholders("{{name}} {{ role }} {{name}}"), ["name", "role"])

    def test_render_template(self):
        self.assertEqual(
            render_template("Hello {{name}}!", {"name": "world"}),
            "Hello world!",
        )

    def test_render_missing_value_fails(self):
        with self.assertRaisesRegex(ValueError, "missing value"):
            render_template("Hello {{name}}", {})

    def test_render_unused_value_fails(self):
        with self.assertRaisesRegex(ValueError, "unused value"):
            render_template("Hello {{name}}", {"name": "A", "extra": "B"})

    def test_invalid_placeholder_is_reported(self):
        self.assertTrue(inspect_template("{{not-valid}}"))

    def test_parse_var_splits_only_first_equals(self):
        self.assertEqual(parse_var("endpoint=https://example.com/?a=b"),
                         ("endpoint", "https://example.com/?a=b"))

    def test_invalid_variable_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid variable name"):
            parse_var("not-valid=value")

    def test_list_prompts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "one.md").write_text("one", encoding="utf-8")
            (root / "two.txt").write_text("not a prompt", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "two.md").write_text("two", encoding="utf-8")
            self.assertEqual(len(list_prompts(root)), 2)


if __name__ == "__main__":
    unittest.main()
