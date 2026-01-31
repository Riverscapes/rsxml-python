"""Testing for the util functions"""

import os
import tempfile
import unittest

from pathlib import Path
from rsxml import util


class UtilTest(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def test_pretty_duration(self):
        """[summary]"""
        self.assertEqual(util.pretty_duration(0), "0.0 seconds")
        self.assertEqual(util.pretty_duration(10), "10.0 seconds")
        self.assertEqual(util.pretty_duration(100), "1:40 minutes")
        self.assertEqual(util.pretty_duration(103.234234), "1:43 minutes")
        self.assertEqual(util.pretty_duration(1000), "16:40 minutes")
        self.assertEqual(util.pretty_duration(10000), "2:46 hours")
        self.assertEqual(util.pretty_duration(100000), "1 days, 3:46 hours")

    def test_batch(self):
        """[summary]"""
        self.assertEqual(
            list(util.batch([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)),
            [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]],
        )

    def test_sizeof_fmt(self):
        """[summary]"""
        self.assertEqual(util.sizeof_fmt(0), "0.0 B")
        self.assertEqual(util.sizeof_fmt(10), "10.0 B")
        self.assertEqual(util.sizeof_fmt(100), "100.0 B")
        self.assertEqual(util.sizeof_fmt(1000), "1000.0 B")
        self.assertEqual(util.sizeof_fmt(10000), "10.0 KB")
        self.assertEqual(util.sizeof_fmt(100000), "100.0 KB")
        self.assertEqual(util.sizeof_fmt(1000000), "1000.0 KB")
        self.assertEqual(util.sizeof_fmt(10000000), "10.0 MB")
        self.assertEqual(util.sizeof_fmt(100000000), "100.0 MB")
        self.assertEqual(util.sizeof_fmt(1000000000), "1000.0 MB")
        self.assertEqual(util.sizeof_fmt(10000000000), "10.0 GB")
        self.assertEqual(util.sizeof_fmt(100000000000), "100.0 GB")
        self.assertEqual(util.sizeof_fmt(1000000000000), "1000.0 GB")
        self.assertEqual(util.sizeof_fmt(10000000000000), "10.0 TB")
        self.assertEqual(util.sizeof_fmt(100000000000000), "100.0 TB")
        self.assertEqual(util.sizeof_fmt(1000000000000000), "1000.0 TB")
        self.assertEqual(util.sizeof_fmt(10000000000000000), "10.0 PB")
        self.assertEqual(util.sizeof_fmt(100000000000000000), "100.0 PB")
        self.assertEqual(util.sizeof_fmt(1000000000000000000), "1000.0 PB")
        self.assertEqual(util.sizeof_fmt(10000000000000000000), "10.0 EB")
        self.assertEqual(util.sizeof_fmt(100000000000000000000), "100.0 EB")
        self.assertEqual(util.sizeof_fmt(1000000000000000000000), "1000.0 EB")
        self.assertEqual(util.sizeof_fmt(10000000000000000000000), "10.0 ZB")
        self.assertEqual(util.sizeof_fmt(100000000000000000000000), "100.0 ZB")

    def test_get_obj_size(self):
        self.assertEqual(util.get_obj_size(None), 16)
        self.assertIn(util.get_obj_size(0), {24, 28})
        self.assertEqual(util.get_obj_size([1, 2, 3, 4]), 200)
        # Object header sizes differ slightly across Python versions/architectures (e.g., 3.12 arm64 vs 3.11 x86_64)
        self.assertIn(util.get_obj_size({"key": "value"}), {230, 238, 286})

    def test_parse_metadata(self):
        """[summary]"""
        self.assertEqual(util.parse_metadata("key=value"), {"key": "value"})
        self.assertEqual(util.parse_metadata("key=value,key2=value2"), {"key": "value", "key2": "value2"})

    def test_safe_makedirs_basic(self):
        """Test standard directory creation and idempotency."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Create a new nested directory
            # Ensure path is deep enough for the sanity check in safe_makedirs
            new_dir = os.path.join(tmpdir, "subdir", "nested")
            util.safe_makedirs(new_dir)
            self.assertTrue(os.path.isdir(new_dir))

            # 2. Idempotency (dir already exists) - should not fail
            util.safe_makedirs(new_dir)
            self.assertTrue(os.path.isdir(new_dir))

    def test_safe_makedirs_conflict(self):
        """Test failure when a file exists with the same name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path_dir = os.path.join(tmpdir, "conflict_dir")
            os.makedirs(file_path_dir)
            file_path = os.path.join(file_path_dir, "conflict_file")

            # Create a dummy file
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("content")

            # Try to create a directory with the same name as the file
            with self.assertRaises(Exception) as cm:
                util.safe_makedirs(file_path)
            self.assertIn("Can't create directory if there is a file of the same name", str(cm.exception))

    def test_safe_makedirs_validation(self):
        """Test safety checks for short or shallow paths."""
        # 1. Invalid short path as string (strict check)
        # "log" is len 3 (< 5) and 1 component (<= 2)
        with self.assertRaises(Exception) as cm:
            util.safe_makedirs("log")
        self.assertIn("Invalid path", str(cm.exception))

        # 2. Invalid short/shallow absolute path
        if os.name == 'nt':
            bad_path = "C:\\a"
        else:
            bad_path = "/a"

        with self.assertRaises(Exception) as cm:
            util.safe_makedirs(bad_path)
        self.assertIn("Invalid path", str(cm.exception))

    def test_safe_makedirs_path_resolution(self):
        """Test that Path objects are resolved to absolute paths, bypassing strict short-path checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Path("logs") -> Resolves to C:\...\logs which is long and safe
                # Note: "logs" as a string would fail the validation check (len < 5)
                p = Path("logs")
                util.safe_makedirs(p)
                self.assertTrue(p.exists())
                self.assertTrue(p.is_dir())
            finally:
                os.chdir(orig_cwd)
