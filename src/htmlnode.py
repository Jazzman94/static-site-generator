from typing import List, Dict

class HTMLNode:
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: List['HTMLNode'] = None,
                 props: Dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html() not implemented")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    """A leaf node in the HTML tree. It has no children and is used to represent a single HTML element with a tag and value."""
    def __init__(self,
                 tag: str,
                 value: str,
                 props: Dict[str, str] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    """A parent node in the HTML tree. It can have children and is used to represent a container for other HTML elements."""
    def __init__(self,
                 tag: str,
                 children: List[HTMLNode],
                 props: Dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")
        
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"