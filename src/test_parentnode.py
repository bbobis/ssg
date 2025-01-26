import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = ParentNode(None, children=[])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertEqual(str(ctx.exception), "tag is required")

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertEqual(str(ctx.exception), "children is required")

    def test_to_html_empty_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertEqual(str(ctx.exception), "children is required")

    def test_to_html_with_one_node(self):
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Learn Python"),
            ],
        )

        expected = "<ul><li>Learn Python</li></ul>"
        self.assertEqual(
            node.to_html(),
            expected,
        )

    def test_to_html_with_multiple_nodes(self):
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Learn Python"),
                LeafNode("li", "Learn Go"),
            ],
        )

        expected = "<ul><li>Learn Python</li><li>Learn Go</li></ul>"
        self.assertEqual(
            node.to_html(),
            expected,
        )

    def test_to_html_with_nested_nodes(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "TODO:"),
                LeafNode(None, "These are my todo tasks"),
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "Learn Python"),
                                LeafNode("li", "Learn Go"),
                            ],
                        ),
                    ],
                    {"class": "bg-gray"},
                ),
            ],
        )
        expected = '<div><h1>TODO:</h1>These are my todo tasks<div class="bg-gray"><ul><li>Learn Python</li><li>Learn Go</li></ul></div></div>'
        self.assertEqual(
            node.to_html(),
            expected,
        )
