import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from textnode import TextNode, TextType


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
        self.assertEqual(node.to_html(), "")

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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_normal(self):
        text_node = TextNode("hello", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "hello")

    def test_text_to_bold(self):
        text_node = TextNode("hello", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<b>hello</b>")

    def test_text_to_italic(self):
        text_node = TextNode("hello", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<i>hello</i>")

    def test_text_to_code(self):
        text_node = TextNode("hello", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<code>hello</code>")

    def test_text_to_link(self):
        text_node = TextNode("To Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(
            html_node.to_html(), '<a href="https://google.com">To Google</a>'
        )

    def test_text_to_image(self):
        text_node = TextNode("Some Image", TextType.IMAGE, "./asserts/img.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(
            html_node.to_html(),
            '<img src="./asserts/img.jpg" alt="Some Image"></img>',
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_with_backticks_for_code(self):
        node = TextNode(
            "This is text with a `code block`",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "code block",
                    TextType.CODE,
                ),
            ],
        )

    def test_with_star_for_italic(self):
        node = TextNode(
            "This is text with an *italic word*",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with an ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "italic word",
                    TextType.ITALIC,
                ),
            ],
        )

    def test_with_double_star_for_bold(self):
        node = TextNode(
            "This is text with a **bolded word**",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "bolded word",
                    TextType.BOLD,
                ),
            ],
        )

    def test_with_backticks_star_double_star(self):
        new_nodes = [
            TextNode(
                "This is text with a **bolded word**, a text with *italic word*, and a text with `code block` in one sentence",
                TextType.NORMAL,
            )
        ]
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "bolded word",
                    TextType.BOLD,
                ),
                TextNode(
                    ", a text with ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "italic word",
                    TextType.ITALIC,
                ),
                TextNode(
                    ", and a text with ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "code block",
                    TextType.CODE,
                ),
                TextNode(
                    " in one sentence",
                    TextType.NORMAL,
                ),
            ],
        )

    def test_with_no_ending_delimiter(self):
        node = TextNode(
            "This is *text* with a **bolded word?",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is *text* with a **bolded word?",
                    TextType.NORMAL,
                ),
            ],
        )

    def test_with_italic_in_bold(self):
        nodes = [
            TextNode(
                "This is *an italic text with a **bolded word** in a sentence*",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            nodes,
            [
                TextNode(
                    "This is ",
                    TextType.NORMAL,
                ),
                TextNode(
                    "an italic text with a ",
                    TextType.ITALIC,
                ),
                TextNode(
                    "bolded word",
                    TextType.BOLD,
                ),
                TextNode(
                    " in a sentence",
                    TextType.ITALIC,
                ),
            ],
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extracting_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extracting_markdown_images_non_image_format(self):
        text = "This is text with a non ![image link] format (https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [],
        )

    def test_extracting_markdown_links(self):
        text = "This is text with a 2 links going to [google](https://google.com) and to [youtube](https://youtube.com) in one sentence"
        images = extract_markdown_links(text)
        self.assertListEqual(
            images,
            [("google", "https://google.com"), ("youtube", "https://youtube.com")],
        )

    def test_extracting_non_markdown_links(self):
        text = "This is text with a link to [google] that is invalid (https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_links(text)
        self.assertListEqual(
            images,
            [],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_without_image(self):
        nodes = [
            TextNode(
                "This is *an italic text with a **bolded word** in a sentence*",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_image(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode(
                    "This is *an italic text with a **bolded word** in a sentence*",
                    TextType.NORMAL,
                )
            ],
        )

    def test_split_nodes_image_in_beginning(self):
        nodes = [
            TextNode(
                "![rick roll](https://i.imgur.com/aKaOqIh.gif) this is an image",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_image(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" this is an image", TextType.NORMAL),
            ],
        )

    def test_split_nodes_image_in_middle(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) in it",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_image(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" in it", TextType.NORMAL),
            ],
        )

    def test_split_nodes_image_in_end(self):
        nodes = [
            TextNode(
                "this is an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_image(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("this is an image ", TextType.NORMAL),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
            ],
        )

    def test_split_nodes_image_multiple(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) in it",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_image(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.NORMAL),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" in it", TextType.NORMAL),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):

    def test_split_nodes_link_in_beginning(self):
        nodes = [
            TextNode(
                "[google](https://google.com) this is a link",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" this is a link", TextType.NORMAL),
            ],
        )

    def test_split_nodes_link_in_middle(self):
        nodes = [
            TextNode(
                "This is text with a [google](https://google.com) link in it",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" link in it", TextType.NORMAL),
            ],
        )

    def test_split_nodes_link_in_end(self):
        nodes = [
            TextNode(
                "this is a link [google](https://google.com)",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("this is a link ", TextType.NORMAL),
                TextNode("google", TextType.LINK, "https://google.com"),
            ],
        )

    def test_split_nodes_link_multiple(self):
        nodes = [
            TextNode(
                "This is text with a [google](https://google.com) link and a [youtube](https://youtube.com) link in it",
                TextType.NORMAL,
            )
        ]
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" link and a ", TextType.NORMAL),
                TextNode("youtube", TextType.LINK, "https://youtube.com"),
                TextNode(" link in it", TextType.NORMAL),
            ],
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_contains_everything(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://google.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
        )
