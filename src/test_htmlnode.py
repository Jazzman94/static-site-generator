from htmlnode import HTMLNode, LeafNode, ParentNode

import unittest



class TestHTMLNode(unittest.TestCase):
    # HTMLNode testing
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
        node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com" target="_blank"')

    # LeafNode testing
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text!")
        self.assertEqual(node.to_html(), "Just text!")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_to_html_special_characters(self):
        node = LeafNode("a", 'Click "me"!', {"href": "https://www.example.com?id=1&value=2"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com?id=1&value=2">Click "me"!</a>')

    # ParentNode testing
    def test_parent_to_html(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent = ParentNode("b", [child1, child2])
        self.assertEqual(parent.to_html(), '<b><p>Hello, world!</p><a href="https://www.google.com">Click me!</a></b>')

    def test_nested_parent_nodes(self):
        grandchild = LeafNode("span", "I'm deeply nested")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), "<section><div><span>I'm deeply nested</span></div></section>")

    def test_parent_with_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")
        
    def test_parent_tag_none_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "test")]).to_html()

if __name__ == "__main__":
    unittest.main()
