from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        #self.props = props


    def to_html(self):
        if self.value == None:
            raise ValueError("no value")

        if self.tag != None and self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        elif self.tag != None and self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return self.value
        

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"