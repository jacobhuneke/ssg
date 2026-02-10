from textnode import *
from leafnode import *
from blocks import *
from htmlnode import *
from parentnode import *
from split_nodes import *


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("TextType is invalid")

#returns a list of nodes all starting with 'li' tags to store in ordered and unordered list parent items
def get_list_nodes(block, block_type):
    spl_new_line = block.split("\n")
    num_lines = len(spl_new_line)
    list_nodes = []
    for spl in spl_new_line:
        if block_type == BlockType.UNORDERED_LIST:
            no_prefix = spl.removeprefix("- ")
        else:
            if num_lines >= 10:
                no_prefix = spl[4:len(spl)]
            else:
                no_prefix = spl[3:len(spl)]
        list_nodes.append(ParentNode("li", text_to_children(no_prefix)))
    return list_nodes

#helper method to format quotes properly
def remove_greater_than(block):
    spl_new_line = block.split("\n")
    new_lines = ""
    for spl in spl_new_line:
        s = spl.removeprefix(">")
        s = s.lstrip(" ") 
        new_lines += " " + s 
    no_leading_space = new_lines.lstrip(" ")
    return no_leading_space

def rem_whitespace_par(block):
    spl_new_line = block.split("\n")
    new_lines = ""
    for spl in spl_new_line:
        s = spl.strip()
        new_lines += s
    return new_lines

#returns the proper html node given a block and its type
def create_block_html(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            block_no_new_lines = block.replace("\n", " ")
            inline_nodes = text_to_children(block_no_new_lines)
            return ParentNode("p", inline_nodes)
        case BlockType.HEADING:
            count = get_header_count(block)
            block_no_tags = block.lstrip("#")
            block_stripped = block_no_tags.lstrip(" ")
            inline_nodes = text_to_children(block_stripped)
            return ParentNode(f"h{count}", inline_nodes)
        case BlockType.CODE:
            no_left = block.lstrip("```")
            no_left = no_left.lstrip("\n")
            no_left = no_left.lstrip(" ")
            no_end = no_left.rstrip("```")
            code_node = LeafNode("code", no_end)
            return ParentNode("pre", [code_node])
        case BlockType.QUOTE:
            lines = remove_greater_than(block)
            inline_nodes = text_to_children(lines)
            return ParentNode("blockquote", inline_nodes)
        case BlockType.UNORDERED_LIST:
            list_nodes = get_list_nodes(block, block_type)
            return ParentNode("ul", list_nodes)
        case BlockType.ORDERED_LIST:
            list_nodes = get_list_nodes(block, block_type)
            return ParentNode("ol", list_nodes)
        case _:
            raise ValueError("invalid blocktype")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

def markdown_to_html_node(markdown):
    parent = ParentNode("div", [], None)
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block != "\n":
            block_type = block_to_block_type(block)
            children.append(create_block_html(block, block_type))
    parent.children = children
    return parent

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING and get_header_count(block) == 1:
            return block.lstrip("# ")
    raise Exception("Error: no h1 headers")
