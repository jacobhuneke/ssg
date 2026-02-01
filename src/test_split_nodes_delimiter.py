import unittest

from split_nodes_delimiter import *
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_one_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))


    def test_two_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("The first thing to print is `print('Hello world!')`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
        self.assertEqual(new_nodes[4], TextNode("print('Hello world!')", TextType.CODE))

    def test_three_nodes_bold(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("The first thing to print is `print('Hello world!')`", TextType.TEXT)
        node3 = TextNode("this message will contain **BOLD MESSAGES `Bold emssages** you know", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        tc = TextNode("BOLD MESSAGES `Bold emssages", TextType.BOLD)
        self.assertEqual(new_nodes[3], tc)
    
    def test_invalid_italic(self):
        node = TextNode("This is _italics text", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    
    def test_valid_italic(self):
        node = TextNode("This is _italics text_ see?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        tr = TextNode("italics text", TextType.ITALIC)
        self.assertEqual(new_nodes[1], tr)

    def test_invalid_texttype(self):
        node = TextNode("This is _italics text_ see?", TextType.TEXT)
        with self.assertRaises(AttributeError):
            new_nodes = split_nodes_delimiter([node], "_", TextType.INVALID)


    def test_no_old_nodes(self):
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter(None, "_", TextType.ITALIC)

    def test_no_old_nodes2(self):
        new_nodes = split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual([], new_nodes)

    def test_code_and_bold(self):
        node = TextNode("This is **text with a** `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes2[1].text_type == TextType.BOLD, True)
        self.assertEqual(new_nodes2[2].text_type == TextType.CODE, True)

if __name__ == "__main__":
    unittest.main()