from enum import Enum


#types a block can be, default is paragraph
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#returns the number of # at beginning of a header block
def get_header_count(block):
    spl = block.split("#")
    count = 0
    for s in spl:
        if s == "":
            count += 1
    return count

def block_to_block_type(block):
    if block.startswith("#") == True and block.startswith("#######") == False:
        return BlockType.HEADING
    elif block.startswith("```\n") == True and block.endswith("```") == True:
        return BlockType.CODE
    quote = True
    unordered = True
    ordered = True
    spl_new_line = block.split("\n")
    for spl in spl_new_line:
        if spl.startswith(">"):
            continue
        else:
            quote = False
    if quote:
        return BlockType.QUOTE
    for spl in spl_new_line:
        if spl.startswith("- "):
            continue
        else:
            unordered = False
    if unordered:
        return BlockType.UNORDERED_LIST
    
    count = 1
    for spl in spl_new_line:
        if spl.startswith(f"{count}. "):
            count += 1
            continue
        else:
            ordered = False
    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    pars = markdown.split("\n\n")
    blocks = []

    for par in pars:
        if par == "":
            continue
        stripped = par.strip()
        strip = stripped.strip("\n")
        blocks.append(stripped)
    
    return blocks