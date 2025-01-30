import re
from typing import Any, Dict, List

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


double_star_delimiter_substitute = "[9fe2c4e9-3f65-4fdb-b24c-02b15259716c]"


def replace_double_star(text: str):
    return text.replace("**", double_star_delimiter_substitute)


def undo_replace_double_star(text: str):
    return text.replace(double_star_delimiter_substitute, "**")


def split_nodes_delimiter(
    old_nodes: List["TextNode"], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        double_star_replaced = False

        if delimiter == "*":
            # temporarily substitute "**"" with [double_star_delimiter_substitute] to avoid false positive matches with "*"
            node_text = replace_double_star(node_text)
            double_star_replaced = True

        # search for the 1st instance of the delimiter
        starting_delimiter_idx = node_text.find(delimiter)

        if starting_delimiter_idx == -1:
            # Can't process node for the given delimiter, move one.
            new_nodes.append(node)
            continue

        # search for the 2nd instance of the delimiter
        ending_delimiter_search_from_idx = starting_delimiter_idx + len(delimiter)
        ending_delimiter_idx = node_text.find(
            delimiter, ending_delimiter_search_from_idx
        )

        if ending_delimiter_idx == -1:
            starting_node = 0
            if len(new_nodes) != 0:
                last_node_text = new_nodes[-1].text
                starting_node = node_text.find(last_node_text) + (len(last_node_text))
            new_nodes.append(TextNode(node_text[starting_node:], node.text_type))
            continue

        # Found a valid delimited text, check if preceding text exists and create a node
        preceding_text = node_text[:starting_delimiter_idx]
        if len(preceding_text) > 0:
            final = (
                undo_replace_double_star(preceding_text)
                if double_star_replaced
                else preceding_text
            )
            new_nodes.append(TextNode(final, node.text_type))

        # slice the delimited text and create a new text node
        delimited_text_start_idx = starting_delimiter_idx + len(delimiter)
        delimited_text = node_text[delimited_text_start_idx:ending_delimiter_idx]
        if len(delimited_text) > 0:
            final = (
                undo_replace_double_star(delimited_text)
                if double_star_replaced
                else delimited_text
            )
            new_nodes.append(TextNode(final, text_type))

        # Recursively call if there are more text
        succeeding_text_start_idx = ending_delimiter_idx + len(delimiter)
        succeeding_text = node_text[succeeding_text_start_idx:]
        if len(succeeding_text) > 0:
            final = (
                undo_replace_double_star(succeeding_text)
                if double_star_replaced
                else succeeding_text
            )
            new_nodes += split_nodes_delimiter(
                [TextNode(final, node.text_type)], delimiter, text_type
            )

    return new_nodes


def extract_markdown_images(text: str):
    # Markdown image has the following syntax ![Alt Text](url)
    return re.findall(r"\!\[(.*?)\]\((http.*?)\)", text)
