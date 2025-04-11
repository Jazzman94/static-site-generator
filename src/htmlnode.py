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