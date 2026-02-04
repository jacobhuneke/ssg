import unittest

from blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mkdown_empty(self):
        mk = ""
        self.assertListEqual(markdown_to_blocks(mk), [])

    def test_no_newlines(self):
        str = markdown_to_blocks("This is a single block.")
        self.assertEqual(str[0], "This is a single block.")

    def test_heading(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_multtag(self):
        block = "#### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_too_many_heading_tags(self):
        block = "######## heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```\n print(python sux)```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_multlines(self):
        block = "```\n x = 10\ny = 4\nprint(x + y)```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_multlines(self):
        block = "```\n x = 10\ny = 4\nprint(x + y)```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_front_invalid(self):
        block = "``` x = 10\ny = 4\nprint(x + y)```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_front_invalid2(self):
        block = "``\n x = 10\ny = 4\nprint(x + y)```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_back_invalid(self):
        block = "```\nx = 10\ny = 4\nprint(x + y)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote1(self):
        block = "> some quote message\n>another quote line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote2(self):
        block = "> some quote message\n>another quote line\n>and another quote line>"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote3(self):
        block = "< some quote message\n>another quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote4(self):
        block = "> some quote message\n >another quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered1(self):
        block = "- some unordered message\n- another unordered line"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered2(self):
        block = "- some unordered message\n- another unordered line\n- something else"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered3(self):
        block = "-some unordered message\n- another unordered line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered4(self):
        block = "- some unordered message\n-another unordered line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered1(self):
        block = "1. some ordered message\n2. another ordered line"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered2(self):
        block = "1. some ordered message\n2. another ordered line\n3. the third line\n4. fourth line\n5. something to end it"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered3(self):
        block = "1. some ordered message\n3. another ordered line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered4(self):
        block = "1. some ordered message\n2.another ordered line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)