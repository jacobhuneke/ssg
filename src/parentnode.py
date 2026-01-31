from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        #self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("value error no tag")

        if self.children == None:
            raise ValueError("value error no kids")
        str = ""
        if self.props == None:
            str = f"<{self.tag}>"
        elif self.props != None:
            str += f"<{self.tag}{self.props_to_html()}>"

        for kid in self.children:
            str += kid.to_html()

        str += f"</{self.tag}>"
        return str