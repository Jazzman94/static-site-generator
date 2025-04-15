from typing import List

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
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
                raise ValueError(f"Closing delimiter '{delimiter}' not found")
            
            pieces.append(TextNode(remaining_text[:end_idx], text_type))
            
            text = remaining_text[end_idx + len(delimiter):]
        
        if text:
            pieces.append(TextNode(text, TextType.TEXT))
        result.extend(pieces)
    
    return result



""" Regex solutuion
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    if not all(isinstance(x, TextNode) for x in old_nodes):
        raise ValueError("Condition that all objects in the old_nodes must be instances of TextNode is not met")
    
    match text_type:
        case TextType.BOLD:
            regex = r"(?:\*\*(.*?)\*\*)|([^*]+)"
        case TextType.ITALIC:
            regex = r"(?:_(.*?)_)|([^_]+)"
        case TextType.CODE:
            regex = r"(?:`(.*?)`)|([^`]+)"
        case _:
            raise ValueError(f"Invalid {text_type} to match, only BOLD, ITALIC and CODE are allowed")

    result = []
    for obj in old_nodes:
        if obj.text_type != TextType.TEXT:
            result.append(obj)
            continue

        matches = re.finditer(regex, obj.text)
        match_looop_result = []
        for match in matches:
            highlighted = match.group(1)
            normal = match.group(2)
            if highlighted is not None:
                match_looop_result.append(TextNode(highlighted, text_type))
            elif normal is not None:
                match_looop_result.append(TextNode(normal, TextType.TEXT))
        result.extend(match_looop_result)
    return result
"""