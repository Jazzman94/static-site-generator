from typing import List, Tuple
import re
from enum import Enum

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_transformer import text_node_to_html_node

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """Parsing of TextType.TEXT nodes to separated TextNodes of TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE."""
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        pieces = []
        
        while delimiter in text:
            start_idx = text.find(delimiter)
            
            if start_idx > 0:
                pieces.append(TextNode(text[:start_idx], TextType.TEXT))
            
            remaining_text = text[start_idx + len(delimiter):]
            end_idx = remaining_text.find(delimiter)
            
            if end_idx == -1:
                pieces.append(TextNode(text[start_idx:], TextType.TEXT))
                text = ""
                break

            pieces.append(TextNode(remaining_text[:end_idx], text_type))
            text = remaining_text[end_idx + len(delimiter):]
        
        if text:
            pieces.append(TextNode(text, TextType.TEXT))
        result.extend(pieces)
    
    return result

def extract_markdown_images(text: str) -> List[Tuple[str,str]]:
    """Extracts regular image links from markdown text."""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text: str) -> List[Tuple[str,str]]:
    """Extracts regular links from markdown text."""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        pieces = []
        
        links = extract_markdown_images(text)
        
        if not links:
            result.append(old_node)
            continue

        for link in links:
            delimiter = f"![{link[0]}]({link[1]})"
            splitted = text.split(delimiter, 1)

            if splitted[0] != "":
                pieces.append(TextNode(splitted[0], TextType.TEXT))
            
            pieces.append(TextNode(link[0], TextType.IMAGE, url=link[1]))
            text = splitted[1] if len(splitted) > 1 else ""
        
        if text != "":
            pieces.append(TextNode(text, TextType.TEXT))
            
        result.extend(pieces)
    
    return result

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        pieces = []
        
        links = extract_markdown_links(text)
        
        if not links:
            result.append(old_node)
            continue

        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            splitted = text.split(delimiter, 1)

            if splitted[0] != "":
                pieces.append(TextNode(splitted[0], TextType.TEXT))
            
            pieces.append(TextNode(link[0], TextType.LINK, url=link[1]))
            text = splitted[1] if len(splitted) > 1 else ""
        
        if text != "":
            pieces.append(TextNode(text, TextType.TEXT))
            
        result.extend(pieces)
    
    return result

def text_to_textnodes(text: str) -> List[TextNode]:
    """Converts a markdown string to a list of TextNode objects."""
    if not text:
        return []
    
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    
    cleaned_blocks = []
    for block in blocks:
        lines = block.split("\n")
        block = "\n".join(map(lambda line: line.strip(), lines))
        if block:  # Only add non-empty blocks
            cleaned_blocks.append(block.strip())
            
    return cleaned_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.ULIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown: str) -> str:
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    # If we get here, no h1 header was found
    raise Exception("No h1 header found in the markdown")



"""
def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level == 1:  # Only extract h1 headings
                return block[level + 1 :].strip()
    return ""
"""