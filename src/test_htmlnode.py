import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value(self):
        node = LeafNode(None, "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")

    def test_to_html_no_props(self):
        node = LeafNode("button", "Click me!")
        self.assertEqual(node.to_html(), "<button>Click me!</button>")

    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


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
