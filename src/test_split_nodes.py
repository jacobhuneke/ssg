import unittest

from split_nodes import *
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
        self.assertEqual(new_nodes2[3].text_type == TextType.CODE, True)

    def test_split_nodes_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
        "and another ![second given image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second given image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )


    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" and ", TextType.TEXT),
             TextNode(
                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
        ],
        new_nodes,
        )

    def test_single_image(self):
        node = TextNode("this is an image test text ![](www.goog.com) ask how it went?", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("this is an image test text ", TextType.TEXT, None),
                TextNode("", TextType.IMAGE, "www.goog.com"),
                TextNode(" ask how it went?", TextType.TEXT, None),
            ],
        )

    def test_two_nodes_image(self):
        node = TextNode("this is an image test text ![](www.goog.com) ask how it went?", TextType.TEXT,)
        node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
        "and another ![second given image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2,])
        self.assertEqual(new_nodes[1], TextNode("", TextType.IMAGE, "www.goog.com"),)
        self.assertEqual(len(new_nodes), 7)

    def test_two_nodes_link(self):
        node = TextNode("this is an image test text [](www.goog.com) ask how it went?", TextType.TEXT,)
        node2 = TextNode(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) "
        "and another [second given image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node2,])
        self.assertEqual(new_nodes[1], TextNode("", TextType.LINK, "www.goog.com"),)
        self.assertEqual(len(new_nodes), 7)

    def test_no_leading_words_image(self):
        node = TextNode("![alt text](some url) and extra words", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("alt text", TextType.IMAGE, "some url"), TextNode(" and extra words", TextType.TEXT, None)
            ],
        )

    def test_no_leading_words_link(self):
        node = TextNode("[alt text](some url) and extra words", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("alt text", TextType.LINK, "some url"), TextNode(" and extra words", TextType.TEXT, None)
            ],
        )

    def test_empty_img(self):
        node = TextNode("![]()", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("", TextType.IMAGE, "")]
        )

    def test_empty_link(self):
        node = TextNode("[]()", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("", TextType.LINK, "")]
        )

    def test_two_links_(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)[to bing](www.bing.com)[to youtube](https://www.youtube.com/@bootdotdev) and some extra words",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 5)
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes,
                                [
                                TextNode("This is ", TextType.TEXT, None), 
                                TextNode("text", TextType.BOLD, None), 
                                TextNode(" with an ", TextType.TEXT, None), 
                                TextNode("italic", TextType.ITALIC, None),
                                TextNode(" word and a ", TextType.TEXT, None), 
                                TextNode("code block", TextType.CODE, None),
                                TextNode(" and an ", TextType.TEXT, None),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.TEXT, None),
                                TextNode("link", TextType.LINK, "https://boot.dev")],
    
                             )
        
    def test_text_to_nodes_ooorder(self):
        text = "**something bold**_something Italic_  `some code`"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(len(new_nodes), 4)

    def test_text_to_nodes2(self):
        text = "this will be out of order **a bog bolded message**, some r a ndom balogna **more bold****more bold**"
        new_nodes = text_to_textnodes(text)
        num_bold = 0
        for node in new_nodes:
            if node.text_type == TextType.BOLD:
                num_bold += 1
        self.assertEqual(3, num_bold)


        
if __name__ == "__main__":
    unittest.main()