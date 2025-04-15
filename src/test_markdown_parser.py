from textnode import TextNode, TextType
from markdown_parser import *
import unittest


class TestHTMLNode(unittest.TestCase):
            
    # Test cases for split_nodes_delimiter function
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
        output = [TextNode("This is text with an ", TextType.TEXT),
                  TextNode("**unclosed bold", TextType.TEXT)]
        result = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual(output, result)

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

    # Test cases for extract_markdown_images and extract_markdown_links functions
    def test_extract_markdown_images(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_images_one_faulty(self):
        input = "This is text with a ![rick roll](https://i. and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_images_no_match(self):
        input = "This is text with no images"
        output = []
        result = extract_markdown_images(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_links(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        result = extract_markdown_links(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_links_one_faulty(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube"
        output = [("to boot dev", "https://www.boot.dev")]
        result = extract_markdown_links(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_links_no_match(self):
        input = "This is text with no links"
        output = []
        result = extract_markdown_links(input)
        
        self.assertEqual(output, result)

    def test_extract_markdown_links_with_images(self):
        input = "This text has a ![image](https://example.com/img.png) and a [link](https://example.com)"
        output = [("link", "https://example.com")]
        result = extract_markdown_links(input)
        
        self.assertEqual(output, result)

    # Test cases for split_nodes_image and split_node_link functions
    def test_split_nodes_links(self):
        input = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        output = [TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]

        result = split_nodes_link([input])
        self.assertEqual(output, result)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_combined_images_links(self):
        input = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        output = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        result = split_nodes_link([input])
        result = split_nodes_image(result)
        self.assertEqual(output, result)

    def test_empty_text_nodes(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual([node], split_nodes_link([node]))
        self.assertEqual([node], split_nodes_image([node]))

    def test_non_text_nodes(self):
        link_node = TextNode("existing link", TextType.LINK, "https://example.com")
        image_node = TextNode("existing image", TextType.IMAGE, "https://example.com/img.png")
        
        self.assertEqual([link_node], split_nodes_link([link_node]))
        self.assertEqual([image_node], split_nodes_image([image_node]))
    
    def test_consecutive_links(self):
        node = TextNode("[link1](https://example1.com)[link2](https://example2.com)", TextType.TEXT)
        expected = [
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode("link2", TextType.LINK, "https://example2.com")
        ]
        self.assertEqual(expected, split_nodes_link([node]))

    def test_consecutive_images(self):
        node = TextNode("![img1](https://img1.png)![img2](https://img2.png)", TextType.TEXT)
        expected = [
            TextNode("img1", TextType.IMAGE, "https://img1.png"),
            TextNode("img2", TextType.IMAGE, "https://img2.png")
        ]
        self.assertEqual(expected, split_nodes_image([node]))

    def test_links_with_special_chars(self):
        node = TextNode("[link with spaces](https://example.com/path with spaces)", TextType.TEXT)
        expected = [
            TextNode("link with spaces", TextType.LINK, "https://example.com/path with spaces")
        ]
        self.assertEqual(expected, split_nodes_link([node]))

    def test_multiple_input_nodes(self):
        node1 = TextNode("Text with [link](https://example.com)", TextType.TEXT)
        node2 = TextNode("Another [link2](https://example2.com) text", TextType.TEXT)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("Another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode(" text", TextType.TEXT),
        ]
        
        self.assertEqual(expected, split_nodes_link([node1, node2]))

    def test_no_links_or_images(self):
        node = TextNode("Plain text without any markup", TextType.TEXT)
        self.assertEqual([node], split_nodes_link([node]))
        self.assertEqual([node], split_nodes_image([node]))

    def test_invalid_markdown_format(self):
        # Missing closing bracket
        node1 = TextNode("Text with [partial link(https://example.com)", TextType.TEXT)
        # Missing opening parenthesis
        node2 = TextNode("Text with [broken link]https://example.com)", TextType.TEXT)
        # Missing closing parenthesis
        node3 = TextNode("Text with [another link](https://example.com", TextType.TEXT)
        # Invalid image format
        node4 = TextNode("Text with !image](https://example.com/img.png)", TextType.TEXT)
        
        # Should remain unchanged since they don't match the expected pattern
        self.assertEqual([node1], split_nodes_link([node1]))
        self.assertEqual([node2], split_nodes_link([node2])) 
        self.assertEqual([node3], split_nodes_link([node3]))
        self.assertEqual([node4], split_nodes_image([node4]))
        
        # Valid and invalid mixed
        mixed_node = TextNode("Valid [link](https://example.com) and [broken](https://broken", TextType.TEXT)
        expected = [
            TextNode("Valid ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and [broken](https://broken", TextType.TEXT)
        ]
        self.assertEqual(expected, split_nodes_link([mixed_node]))

    # Test cases for text_to_textnodes function
    def test_mdtext_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")]
        result = text_to_textnodes(input)
        self.assertEqual(output, result)

    # Test cases for markdown_to_blocks function
    def test_markdown_to_blocks(self):
        md = """
    # This is header

    ```
    code
    code
    code
    ```

    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is header",
                "```\ncode\ncode\ncode\n```",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading level 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading level 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading level 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Invalid heading"), BlockType.PARAGRAPH)

        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('Hello!')\n```"), BlockType.CODE)

        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)

        self.assertEqual(block_to_block_type("- Item in unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- "), BlockType.UNORDERED_LIST)

        self.assertEqual(block_to_block_type("1. First item in ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("10. Another item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1 item without dot"), BlockType.PARAGRAPH)

        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()