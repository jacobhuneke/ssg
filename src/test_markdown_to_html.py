import unittest
from text_node_to_html_node import *

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraph_block(self):
        md = "some paragraph with a new line\nthe new line "
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].children[0].value, "some paragraph with a new line the new line")

    def test_header_block(self):
        md = "### a header3 node no par"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "h3")

    def test_code_block(self):
        md = "```\n x = 10\ny = 4\nprint(x + y)```"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].children[0].value, "x = 10\ny = 4\nprint(x + y)")

    def test_quote_block(self):
        md = "> some quote message\n> another quote line"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].children[0].value, "some quote message another quote line")

    def test_unordered_list(self):
        md = "- some unordered message\n- another **unordered** line"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].children[0].children[0].value, "some unordered message")
    
    def test_ordered_list_block(self):
        md = "1. some ordered message\n2. another ordered line\n3. the third line\n4. fourth line\n5. something to end it"
        node = markdown_to_html_node(md)
        self.assertEqual(len(node.children[0].children), 5)
        
    def test_italics_par(self):
        md = "This is _italics text_**see?**"
        node = markdown_to_html_node(md)
        #print(node)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """       
> some quote will be here with `code in a block and more code`
> and another quote line
> and some more quotes**in bold**
> _in italic_
> ![args](somesite.url)
> end of quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(html, '<div><blockquote>some quote will be here with <code>code in a block and more code</code> and another quote line and some more quotes<b>in bold</b> <i>in italic</i> <img src="somesite.url" alt="args"> end of quote</blockquote></div>')

    def test_headerblock(self):
        md = """
### the header contains **BIG BOLDED WORDS** and a link [link arg](link url.com)

- also an unordered list `code`
- some _italic_ line
- something else in a line

and a paragraph here containing nothing but words
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         '<div><h3>the header contains <b>BIG BOLDED WORDS</b> and a link <a href="link url.com">link arg</a></h3><ul><li>also an unordered list <code>code</code></li><li>some <i>italic</i> line</li><li>something else in a line</li></ul><p>and a paragraph here containing nothing but words</p></div>')
        
    def test_ordered_block(self):
        md = """
1. some first `code`
2. still in the code
3. a **bold** element

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(node.children[0].tag, "ol")

    def test_by_lainey(self):
        md = """
> i dont even know it! Hey!! **HEYYY!!!!** _hehehehehehehehehahhahahahahahahahahaha_
>im gonna kiss you
>can you write a test for how amny kisses i give you in a day

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><blockquote>i dont even know it! Hey!! <b>HEYYY!!!!</b> <i>hehehehehehehehehahhahahahahahahahahaha</i> im gonna kiss you can you write a test for how amny kisses i give you in a day</blockquote></div>')

    def test_empty_block(self):
        md = ''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_only_nl(self):
        md = "\n\n \n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p></p></div>")

    def test_four_headers(self):
        md = """
# first head

## second head

### third head

#### fourth head

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><h1>first head</h1><h2>second head</h2><h3>third head</h3><h4>fourth head</h4></div>')

    def test_mult_nls(self):
        md = """


some text in a paragraph



> a quote block
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><p>some text in a paragraph</p><blockquote>a quote block</blockquote></div>')

    def test_code_endnl(self):
        md = """
```
# This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><pre><code># This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>')

    def test_nested_quotes(self):
        md = """
> Outer
> > Inner
> > Still inner
> Back to outer
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><blockquote>Outer > Inner > Still inner Back to outer</blockquote></div>')