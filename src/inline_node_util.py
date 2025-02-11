import re
from typing import List

from textnode import TextNode, TextType

double_star_delimiter_substitute = "[9fe2c4e9-3f65-4fdb-b24c-02b15259716c]"


def replace_double_star(text: str):
    return text.replace("**", double_star_delimiter_substitute)


def undo_replace_double_star(text: str):
    return text.replace(double_star_delimiter_substitute, "**")


def split_nodes_delimiter(
    old_nodes: List["TextNode"], delimiter: str, text_type: TextType
) -> List["TextNode"]:
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


def split_nodes_image(old_nodes: List["TextNode"]) -> List["TextNode"]:
    return split_nodes_image_or_link(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes: List["TextNode"]) -> List["TextNode"]:
    return split_nodes_image_or_link(old_nodes, TextType.LINK)


def extract_markdown_images(text: str):
    # Markdown image has the following syntax ![Alt Text](url)
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str):
    # Markdown link has the following syntax [Link Text](url)
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image_or_link(old_nodes: List["TextNode"], text_type: TextType):
    if text_type not in [TextType.IMAGE, TextType.LINK]:
        raise ValueError("Invalid text type")

    new_nodes = []

    extractor = (
        extract_markdown_images
        if text_type == TextType.IMAGE
        else extract_markdown_links
    )

    def formatter(text, url):
        formatted = f"[{text}]({url})"
        return formatted if text_type == TextType.LINK else "!" + formatted

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        extracted_text_and_url = extractor(node.text)
        if len(extracted_text_and_url) == 0:
            new_nodes.append(node)
            continue

        search_from_idx = 0

        for i in range(len(extracted_text_and_url)):
            text_to_search = node.text[search_from_idx:]

            text, url = extracted_text_and_url[i]
            image_substring = formatter(text, url)
            image_substring_idx = text_to_search.find(image_substring)

            # Check preceding
            if image_substring_idx != 0:
                preceding_text = text_to_search[:image_substring_idx]
                new_nodes.append(TextNode(preceding_text, TextType.NORMAL))

            new_nodes.append(TextNode(text, text_type, url))

            # Move starting pointer
            search_from_idx = image_substring_idx + len(image_substring)

            if i == len(extracted_text_and_url) - 1:
                # check succeeding
                if search_from_idx == len(text_to_search):
                    break
                succeeding = text_to_search[search_from_idx:]
                new_nodes.append(TextNode(succeeding, TextType.NORMAL))

    return new_nodes


def text_to_text_nodes(text) -> List["TextNode"]:
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
