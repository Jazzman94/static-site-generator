from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL must be provided for LINK type")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL must be provided for IMAGE type")
            if not text_node.text:
                text_node.text = "Image without description"
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
