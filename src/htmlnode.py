
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not Implemented")

    def props_to_html(self):
        formatted_str = ""
        if self.props != None and self.props != {}:
            for prop in self.props:
                formatted_str += f' {prop}="{self.props[prop]}"' 
        return formatted_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"