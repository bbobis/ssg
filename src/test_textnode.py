import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("Code text", TextType.CODE)
        node2 = TextNode("Italic text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("url1", TextType.LINK, "http://some-url.com")
        node2 = TextNode("url1", TextType.LINK, "http://some-url.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
