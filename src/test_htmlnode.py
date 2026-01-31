import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_const(self):
        node = HTMLNode("a", "The words inside the paragraph", props={"href": "https://www.google.com"})
        node2 = HTMLNode("a", "The words inside the paragraph", node, props={"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode("a", "The words inside the paragraph", props={"href": "https://www.google.com"})
        html = node.props_to_html()
        str = ' href="https://www.google.com"'
        self.assertEqual(html, str)
    
    def test_props_to_html_none(self):
        node = HTMLNode("p", "The words inside the paragraph")
        str = ""
        html = node.props_to_html()
        self.assertEqual(html, str)

    def test_repr(self):
        node = HTMLNode("a", "The words inside the paragraph", props={"href": "https://www.google.com"})
        str = node.__repr__()
        str2 = "HTMLNode(a, The words inside the paragraph, None, {'href': 'https://www.google.com'})"
        self.assertEqual(str, str2)