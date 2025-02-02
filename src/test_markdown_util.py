import unittest

from markdown_util import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_no_title(self):
        with self.assertRaises(Exception) as ctx:
            extract_title("## This is not the main title")
        self.assertEqual(str(ctx.exception), "No title found")

    def test_with_title(self):
        title = extract_title("# This is the main title  ")
        self.assertEqual(title, "This is the main title")
