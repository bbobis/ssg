import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_None(self):
        node = HTMLNode("p", "hello")
        actual = node.props_to_html()
        expected = ""
        self.assertEqual(actual, expected)

    def test_props_to_html_single(self):
        node = HTMLNode("p", "hello", props={"a": "1"})
        actual = node.props_to_html()
        expected = 'a="1"'
        self.assertEqual(actual, expected)

    def test_props_to_html_multiple(self):
        node = HTMLNode("p", "hello", props={"a": "1", "b": 2})
        actual = node.props_to_html()
        expected = 'a="1" b="2"'
        self.assertEqual(actual, expected)
