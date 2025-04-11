from htmlnode import HTMLNode
from textnode import TextNode, TextType

import unittest



class TestHTMLNode(unittest.TestCase):
    # props testing
    def test_props_eq(self):
        node = HTMLNode(props =  {"class": "test"})
        node2 = HTMLNode(props = {"class": "test"})
        self.assertTrue(node.props_to_html() == node2.props_to_html())

    def test_props_not_eq(self):
        node = HTMLNode(props = {"class": "test"})
        node2 = HTMLNode(props = {"class": "test2"})
        self.assertFalse(node.props_to_html() == node2.props_to_html())

    def test_props_eq_one_no_props(self):
        node = HTMLNode(props = {"class": "test"})
        node2 = HTMLNode()
        self.assertFalse(node.props_to_html() == node2.props_to_html())

    def test_props_eq_no_props(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertTrue(node.props_to_html() == node2.props_to_html())

    def test_props_eq_to_example(self):
        example = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node.props_to_html() == example)

if __name__ == "__main__":
    unittest.main()
