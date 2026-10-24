"""Tests for LeakCheck's safe reporting and file traversal."""
import tempfile
import unittest
from pathlib import Path

from leakcheck import iter_files, scan_file


class LeakCheckTests(unittest.TestCase):
    def test_detects_key_without_returning_secret(self):
        secret = "AKIA1234567890ABCDEF"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("key = " + secret, encoding="utf-8")
            findings = scan_file(path)
        self.assertEqual(findings, [(1, "AWS access key ID")])
        self.assertNotIn(secret, repr(findings))

    def test_detects_private_key_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "key.pem"
            path.write_text("-----BEGIN PRIVATE KEY-----", encoding="utf-8")
            self.assertEqual(scan_file(path), [(1, "Private key header")])

    def test_ignores_binary_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "binary.bin"
            binary.write_bytes(b"\xff\xfe")
            oversized = Path(directory) / "large.txt"
            oversized.write_bytes(b"x" * 1_000_001)
            self.assertEqual(scan_file(binary), [])
            self.assertEqual(scan_file(oversized), [])

    def test_skips_common_generated_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "node_modules").mkdir()
            (root / "node_modules" / "ignored.js").write_text("hello", encoding="utf-8")
            (root / "app.py").write_text("print('hello')", encoding="utf-8")
            paths = {p.name for p in iter_files(root)}
            self.assertEqual(paths, {"app.py"})


if __name__ == "__main__":
    unittest.main()
