"""Unit tests for the dependency-free DevKit utilities."""
import unittest

from devkit import (
    base64_decode, base64_encode, format_json, iso_to_timestamp,
    minify_json, timestamp_to_iso, url_decode, url_encode,
)


class DevKitTests(unittest.TestCase):
    def test_json_format(self):
        self.assertEqual(format_json('{"hello":"world"}'), '{\n  "hello": "world"\n}')

    def test_json_minify(self):
        self.assertEqual(minify_json('{ "a": 1, "b": [2, 3] }'), '{"a":1,"b":[2,3]}')

    def test_invalid_json_raises(self):
        with self.assertRaises(ValueError):
            format_json("{bad json}")

    def test_url_round_trip(self):
        value = "hello world & tea"
        self.assertEqual(url_decode(url_encode(value)), value)

    def test_url_form_round_trip(self):
        value = "hello world & tea"
        self.assertEqual(url_decode(url_encode(value, form=True), form=True), value)

    def test_base64_round_trip_unicode(self):
        value = "KIHMT Tech Labs — नमस्ते"
        self.assertEqual(base64_decode(base64_encode(value)), value)

    def test_invalid_base64_raises(self):
        with self.assertRaises(ValueError):
            base64_decode("%%%")

    def test_timestamp_to_iso_epoch(self):
        self.assertEqual(timestamp_to_iso("0"), "1970-01-01T00:00:00Z")

    def test_iso_to_timestamp_epoch(self):
        self.assertEqual(iso_to_timestamp("1970-01-01T00:00:00Z"), "0.0")

    def test_iso_requires_timezone(self):
        with self.assertRaises(ValueError):
            iso_to_timestamp("2026-01-01T12:00:00")


if __name__ == "__main__":
    unittest.main()
