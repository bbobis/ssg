import unittest

from block_node_util import BlockType, block_to_block_type, markdown_to_block


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        blocks = markdown_to_block(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels(self):
        text = "# heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "## heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "### heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "#### heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "##### heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "###### heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        text = "####### heading"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        text = "#heading"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_code_block(self):
        text = "```code block```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
        text = """```
                code block
        ```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote_block(self):
        text = "> quotes 1\n>quote 2"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
        text = "+ quotes 1\n>quote 2"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        text = "* list 1\n* list"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
        text = "- list 1\n- list"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
        text = "- list 1\n* list"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
        text = "-list 1\n*list"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        text = "1. list 1\n2. list"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
        text = "0. list 1"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        text = "1.list 1"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        text = "a. list 1"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
