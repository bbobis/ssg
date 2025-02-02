import re
from typing import Any, Dict, List

from block_node_util import BlockType, block_to_block_type, markdown_to_block
from inline_node_util import text_to_text_nodes
from textnode import TextNode, TextType


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, Any] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join(map(lambda item: f'{item[0]}="{item[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):

    def __init__(
        self,
        tag: str | None,
        children: List["HTMLNode"] | None,
        props: Dict[str, Any] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children or len(self.children) == 0:
            raise ValueError("children is required")

        children_as_html = self.__children_to_html(self.children)
        props = self.props_to_html()
        props = props if props == "" else f" {props}"
        return f"<{self.tag}{props}>{children_as_html}</{self.tag}>"

    def __children_to_html(self, children: List["HTMLNode"]):
        if len(children) == 0:
            return ""
        result = self.__children_to_html(children[1:])
        return children[0].to_html() + result

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(
        self, tag: str | None, value: str, props: Dict[str, Any] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if not self.tag:
            return self.value
        props = self.props_to_html()
        props = props if props == "" else f" {props}"
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


def text_node_to_html_node(text_node: TextNode):
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def markdown_to_html_node(markdown: str):
    children: List["HTMLNode"] = []

    blocks = markdown_to_block(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.HEADING:
                children.append(markdown_heading_to_html(block))
            case BlockType.CODE:
                children.append(markdown_code_block_to_html(block))
            case BlockType.UNORDERED_LIST:
                children.append(markdown_unordered_list_to_html(block))
            case BlockType.ORDERED_LIST:
                children.append(markdown_ordered_list_to_html(block))
            case BlockType.QUOTE:
                children.append(markdown_quote_block_to_html(block))
            case BlockType.PARAGRAPH:
                children.append(markdown_paragraph_block_to_html(block))
            case _:
                raise ValueError("Invalid block")

    return ParentNode("div", children)


def markdown_heading_to_html(heading: str) -> ParentNode:
    tag = f"h{heading.count("#")}"
    text = heading.replace("#", "").strip()
    children = list(map(text_node_to_html_node, text_to_text_nodes(text)))
    return ParentNode(tag, children)


def markdown_code_block_to_html(code_block: str) -> LeafNode:
    return LeafNode("pre", code_block.replace("```", "").strip())


def markdown_unordered_list_to_html(ul_block: str) -> ParentNode:
    list_items = ul_block.splitlines()
    children = list(map(line_to_html_list_item, list_items))
    return ParentNode("ul", children)


def markdown_ordered_list_to_html(ul_block: str) -> ParentNode:
    list_items = ul_block.splitlines()
    children = list(map(line_to_html_list_item, list_items))
    return ParentNode("ol", children)


def line_to_html_list_item(line: str):
    text = re.sub(r"^[\d*-]*\.*\s", "", line).strip()
    children = list(map(text_node_to_html_node, text_to_text_nodes(text)))
    return ParentNode("li", children)


def markdown_quote_block_to_html(quote_block: str) -> ParentNode:
    quotes = quote_block.splitlines()
    for quote in quotes:
        text = quote.replace(">", "", 1).strip()
        children = list(map(text_node_to_html_node, text_to_text_nodes(text)))
    return ParentNode("blockquote", children)


def markdown_paragraph_block_to_html(paragraph_block: str) -> ParentNode:
    children = list(map(text_node_to_html_node, text_to_text_nodes(paragraph_block)))
    return ParentNode("p", children)
