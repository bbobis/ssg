import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_block(markdown: str):
    blocks = []
    for block in markdown.split("\n\n"):
        blocks.append("\n".join(map(lambda s: s.strip(), block.strip().split("\n"))))
    return blocks


def block_to_block_type(markdown_block_text: str):
    total_lines = len(markdown_block_text.split("\n"))

    if len(re.findall(r"^\#{1,6}\s.+", markdown_block_text, re.M)) == total_lines:
        return BlockType.HEADING

    if re.findall(r"^`{3}[\s\S]+`{3}$", markdown_block_text, re.M):
        return BlockType.CODE

    if len(re.findall(r"^>\s*.+$", markdown_block_text, re.M)) == total_lines:
        return BlockType.QUOTE

    if len(re.findall(r"^[*-]\s.+$", markdown_block_text, re.M)) == total_lines:
        return BlockType.UNORDERED_LIST

    if (
        len(re.findall(r"^[123456789]+[\d]*\.\s.+$", markdown_block_text, re.M))
        == total_lines
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
