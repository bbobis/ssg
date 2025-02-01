import unittest

from inline_node_util import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
from textnode import TextNode, TextType


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
        nodes = text_to_text_nodes(text)
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
