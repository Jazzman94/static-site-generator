import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        node = TextNode("This is an url node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is an url node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_non_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a different text node", TextType.BOLD, url = None)
        self.assertNotEqual(node, node2)

    def test_non_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_non_eq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_to_example(self):
        node = TextNode("This is a text node", TextType.BOLD)
        example = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), example)
    
    def test_eq_to_example_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        example = "TextNode(This is a text node, link, https://www.boot.dev)"
        self.assertEqual(repr(node), example)


if __name__ == "__main__":
    unittest.main()
