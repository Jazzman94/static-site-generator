from typing import List, Tuple
import re

from textnode import TextNode, TextType

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