from textnode import TextNode, TextType
from splitter import split_nodes_delimiter
import unittest


class TestHTMLNode(unittest.TestCase):
            
    def test_eq_one_bold(self):
        input = TextNode("This is text with a **bolded phrase** in the middle",TextType.TEXT)
        output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input], "**", TextType.BOLD)
        
        self.assertEqual(output, result)

    def test_eq_three_italic(self):
        input = TextNode("This is text _with_ a _bolded_ phrase _in_ the middle",TextType.TEXT)
        output = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("with", TextType.ITALIC),
            TextNode(" a ", TextType.TEXT),
            TextNode("bolded", TextType.ITALIC),
            TextNode(" phrase ", TextType.TEXT),
            TextNode("in", TextType.ITALIC),
            TextNode(" the middle", TextType.TEXT),]
        result = split_nodes_delimiter([input], "_", TextType.ITALIC)
        
        self.assertEqual(output, result)

    def test_more_nodes(self):
        input = [
            TextNode("This is text _with_ a _italic_ phrase _in_ the middle",TextType.TEXT),
            TextNode("This is text with a _italic_ in the middle",TextType.TEXT)]
        output = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("with", TextType.ITALIC),
            TextNode(" a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" phrase ", TextType.TEXT),
            TextNode("in", TextType.ITALIC),
            TextNode(" the middle", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT)]

        result = split_nodes_delimiter(input, "_", TextType.ITALIC)
        
        self.assertEqual(output, result)

    def test_missing_closing_delimiter(self):
        input = TextNode("This is text with an **unclosed bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input], "**", TextType.BOLD)

    def test_code_delimiter(self):
        input = TextNode("This is text with a `code block` in it", TextType.TEXT)
        output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input], "`", TextType.CODE)
        
        self.assertEqual(output, result)

    def test_empty_input(self):
        result = split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual([], result)

    def test_no_delimiter_in_text(self):
        input = TextNode("This text has no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual([input], result)

    def test_multiple_delimiter_types_in_sequence(self):
        input = TextNode("This has _italic_ and **bold** text", TextType.TEXT)
        
        after_italic = split_nodes_delimiter([input], "_", TextType.ITALIC)
        expected_after_italic = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and **bold** text", TextType.TEXT)
        ]
        self.assertEqual(expected_after_italic, after_italic)
        
        after_bold = split_nodes_delimiter(after_italic, "**", TextType.BOLD)
        expected_final = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(expected_final, after_bold)

if __name__ == "__main__":
    unittest.main()