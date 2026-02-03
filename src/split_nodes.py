from textnode import *
from extract import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes is None:
        raise ValueError("no old nodes")
    if delimiter is None:
        raise ValueError("no delimiter")

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        spl = node.text.split(delimiter)
        #[this is text with a , code block, word]
        #len = 
        if len(spl) % 2 == 0:
            raise Exception("invalid markdown syntax")
    
        i = 0
        for s in spl:
            if s == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(s, TextType.TEXT))
            else:
                new_nodes.append(TextNode(s, text_type))
            i += 1

    return new_nodes


def split_nodes_image(old_nodes):
    if old_nodes == None:
        raise ValueError("no old nodes")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_matches = extract_markdown_images(node.text)
        if image_matches == []:
            new_nodes.append(node)
            continue
        str = node.text
        for image in image_matches:
            spl = str.split(f"![{image[0]}]({image[1]})", 1)
            if len(spl) != 2:
                raise ValueError("invalid markdown syntax")
            if spl[0] != "":
                new_nodes.append(TextNode(spl[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            str = spl[1]
        if str != "":
            new_nodes.append(TextNode(spl[1], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    if old_nodes == None:
        raise ValueError("no old nodes")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_matches = extract_markdown_link(node.text)
        if len(link_matches) == 0:
            new_nodes.append(node)
            continue
        str = node.text
        for link in link_matches:
            spl = str.split(f"[{link[0]}]({link[1]})", 1)
            if len(spl) != 2:
                raise ValueError("invalid markdown syntax")
            if spl[0] != "":
                new_nodes.append(TextNode(spl[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            str = spl[1]
        if str != "":
            new_nodes.append(TextNode(spl[1], TextType.TEXT))
    return new_nodes