import unittest

from textnode import TextNode, TextType
from node_transformer import text_node_to_html_node


class TestNodeTransformer(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props.get("href"), "https://example.com")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props.get("src"), "https://example.com/image.jpg")
        self.assertEqual(html_node.props.get("alt"), "Alt text")

    def test_unknown_type(self):
        node = TextNode("This is unknown", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
        
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_missing_url_for_link(self):
        node = TextNode("Missing URL", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_url_for_image(self):
        node = TextNode("Missing URL", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


        
if __name__ == "__main__":
    unittest.main()
