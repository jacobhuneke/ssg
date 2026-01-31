import unittest

from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", props={"href": "https://www.google.com"})
        str = "LeafNode(p, Hello, world!, {'href': 'https://www.google.com'})"
        self.assertEqual(node.__repr__(), str)

    def test_to_html_notag(self):
        node = LeafNode(None, "value is value")
        str = "value is value"
        self.assertEqual(str, node.to_html())

    def test_to_html_props(self):
        node = LeafNode("a", "Value is value you know", props={"abc": "boot.dev"})
        str = '<a abc="boot.dev">Value is value you know</a>'
        self.assertEqual(node.to_html(), str)