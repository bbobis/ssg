import re
import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    markdown_to_html_node,
    text_node_to_html_node,
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


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_should_be_wrapped_in_div(self):
        markdown = "Learning python"
        html_node = markdown_to_html_node(markdown)
        self.assertRegex(html_node.to_html(), r"^<div>.+</div>$")

    def test_should_handle_different_html_headers(self):
        markdown = """
        # Heading 1
            
        ## Heading 2

        ### Heading 3

        #### Heading 4
        
        ##### Heading 5
        
        ###### Heading 6
        """

        actual = markdown_to_html_node(markdown).to_html()
        expected = prepare(
            """
        <div>
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <h5>Heading 5</h5>
            <h6>Heading 6</h6>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_different_text_types_in_headers(self):
        markdown = """
        # Heading 1 **with bold**
            
        ## Heading 2 *with italic*

        ### Heading 3 `with code`

        #### Heading 4 ![rick roll](https://i.imgur.com/aKaOqIh.gif)
        
        ##### Heading 5 [google](https://google.com)
        """
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <h1>Heading 1 <b>with bold</b></h1>
            <h2>Heading 2 <i>with italic</i></h2>
            <h3>Heading 3 <code>with code</code></h3>
            <h4>Heading 4 <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></h4>
            <h5>Heading 5 <a href="https://google.com">google</a></h5>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_code_blocks(self):
        markdown = """
        ```
        is_code_block = True
        ```
        
        ```
        another_code_block = True
        ```
        """
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <pre>
                is_code_block = True
            </pre>
            <pre>
                another_code_block = True
            </pre>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_unordered_list(self):
        self.maxDiff = None
        markdown = """
        - list item **with bold**
        - list item *with italic*
        * list item `with code`
        * list item with image ![rick roll](https://i.imgur.com/aKaOqIh.gif)
        * list item with link [google](https://google.com)
        """
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <ul>
                <li>list item <b>with bold</b></li>
                <li>list item <i>with italic</i></li>
                <li>list item <code>with code</code></li>
                <li>list item with image <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></li>
                <li>list item with link <a href="https://google.com">google</a></li>
            </ul>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_ordered_list(self):
        self.maxDiff = None
        markdown = """
        1. list item **with bold**
        2. list item *with italic*
        3. list item `with code`
        4. list item with image ![rick roll](https://i.imgur.com/aKaOqIh.gif)
        5. list item with link [google](https://google.com)
        """
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <ol>
                <li>list item <b>with bold</b></li>
                <li>list item <i>with italic</i></li>
                <li>list item <code>with code</code></li>
                <li>list item with image <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></li>
                <li>list item with link <a href="https://google.com">google</a></li>
            </ol>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_quote_block(self):
        self.maxDiff = None
        markdown = """
        > quote **with bold**

        > quote *with italic*
        
        > quote `with code`
        
        > quote with image ![rick roll](https://i.imgur.com/aKaOqIh.gif)
        
        > quote with link [google](https://google.com)
        """
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <blockquote>quote <b>with bold</b></blockquote>
            <blockquote>quote <i>with italic</i></blockquote>
            <blockquote>quote <code>with code</code></blockquote>
            <blockquote>quote with image <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></blockquote>
            <blockquote>quote with link <a href="https://google.com">google</a></blockquote>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )

    def test_should_handle_paragraph_block(self):
        self.maxDiff = None
        markdown = "This is a paragraph with **with bold**, *with italic*, `with code`, with image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and with link [google](https://google.com)"
        actual = markdown_to_html_node(markdown).to_html()

        expected = prepare(
            """
        <div>
            <p>This is a paragraph with <b>with bold</b>, <i>with italic</i>, <code>with code</code>, with image <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img> and with link <a href="https://google.com">google</a></p>
        </div>
        """
        )

        self.assertEqual(
            actual,
            expected,
        )


def prepare(node: str):
    return re.sub(
        r"\s{2,}",
        "",
        node,
    )
