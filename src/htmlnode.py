

class HTMLNode:
    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method is not implemented\
                                   in the parent class HTMLNode")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        output = ""
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'
        return output
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        return False
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str = None, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node does not have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        ):
            return True
        return False
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"