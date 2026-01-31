import unittest

from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_2kids(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("a", "kid2", {"good": "https.goodstuff.com"})
        parent_node = ParentNode("div", children=[child_node, child_node_2])
        str = '<div><span>child</span><a good="https.goodstuff.com">kid2</a></div>'
        self.assertEqual(parent_node.to_html(), str)
    
    def test_to_html_3kids(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("a", "kid2", {"good": "https.goodstuff.com"})
        child_node_3 = LeafNode(None, "kid3 is here", {"url3": "youtube.com"})
        parent_node = ParentNode("div", children=[child_node, child_node_2, child_node_3])
        str = '<div><span>child</span><a good="https.goodstuff.com">kid2</a>kid3 is here</div>'
        self.assertEqual(parent_node.to_html(), str)

    def test_to_html_no_kids(self):
        parent_node = ParentNode("div", None, {"good": "good.com"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_nogkid(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        str = '<div><span></span></div>'
        self.assertEqual(parent_node.to_html(), str)

    def test_to_html_child_w_nokids(self):
        child_node = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_2kids_2gkids(self):
        child_node = LeafNode("span", "kid1")
        child_node_2 = LeafNode("a", "kid2 with tag", {"good": "https.goodstuff.com"})
        child_node_3 = LeafNode(None, "kid3 no tag", {"url3": "youtube.com"})
        parent_node = ParentNode("div", children=[child_node, child_node_2, child_node_3])
        parent_node2 = ParentNode("cent", [parent_node, child_node], {'good': 'good.com'})
        str = '<cent good="good.com"><div><span>kid1</span><a good="https.goodstuff.com">kid2 with tag</a>kid3 no tag</div><span>kid1</span></cent>'
        self.assertEqual(parent_node2.to_html(), str)