from textnode import *
from extract import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes == None:
        raise ValueError("no old nodes")
    if delimiter == None:
        raise ValueError("no delimiter")

    new_nodes = []

    #iterates through every node
    for node in old_nodes:
        #adds to new_nodes if already text type, work is done
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #splits the text string into an array of words and identifies the 
        #starting and ending word of the substring marked by the delimiter
        spl = node.text.split()
        starting_index = 0
        ending_index = 0
        count = 0
        first_del = False
        second_del = False

        for word in spl:
            if word.startswith(delimiter):
                starting_index = count
                first_del = True
            if word.endswith(delimiter):
                ending_index = count
                second_del = True
            count += 1

        #if starting and ending are 0, the delimiter is not present and the node should be returned
        if first_del == False and second_del == False:
            new_nodes.append(node)
            continue
        elif first_del == True and second_del == False:
            raise Exception("invalid markdown syntax")
        elif first_del == False and second_del == True:
            new_nodes.append(node)
            continue
        else:
        #if starting index is 0, the delimiter begins the string, so there is no need to create a text node for the beginning
            if starting_index != 0 and first_del:
                first = TextNode(" ".join(spl[:starting_index]) + " ", TextType.TEXT)
                new_nodes.append(first)

            #creates an array for the delimiter marked substring, removes the delimiter, and joins it back into a string
            #then creates a new text node and adds it to the list
            mid = spl[starting_index : ending_index + 1]
            mid[0] = mid[0].lstrip(delimiter)
            mid[len(mid) - 1] = mid[len(mid) - 1].rstrip(delimiter)
            mid_node = TextNode(' '.join(mid), text_type)  
            new_nodes.append(mid_node)

            #if the ending index is the length of the string, then there is no need to create a text node for the end
            if ending_index + 1 != len(spl) and second_del:
                last = TextNode(" " + " ".join(spl[ending_index + 1:]), TextType.TEXT)
                new_nodes.append(last)
            
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

        str = node.text.split()
        first_del = "!["
        second_del = ")"
        arr = []
        num_images = len(image_matches)
        count = 0
        beginning = True
        in_alt = False
        #iterates through words in sentence
        for s in str:
            #adds word to arr if doesnt begin or end with delimiters for images
            if s.startswith(first_del) == False and s.endswith(second_del) == False and in_alt == False:
                arr.append(s)
            elif s.startswith(first_del):
                in_alt = True
                #adds the leading text, adds a space only at end if beginning of sentence and one before and after if in middle
                if beginning == True and arr != []:
                    new_nodes.append(TextNode(" ".join(arr) + " ", TextType.TEXT))
                    beginning = False
                elif arr != []:
                    new_nodes.append(TextNode(" " + " ".join(arr) + " ", TextType.TEXT))
                
                #resets the array, adds the image text node to the new nodes and preps for next image
                arr = []
                new_nodes.append(TextNode(image_matches[count][0], TextType.IMAGE, image_matches[count][1]))
                count += 1

            first_del_count = s.count(first_del)
            while first_del_count > 0 and s.startswith(first_del) == False:
                new_nodes.append(TextNode(image_matches[count][0], TextType.IMAGE, image_matches[count][1]))
                count += 1
                first_del_count -= 1

            if s.endswith(second_del) == True:
                in_alt = False
        #adds text node w/ leading space if there are any more words in the text
        if arr != []:
            new_nodes.append(TextNode(" " +" ".join(arr), TextType.TEXT))

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
        if link_matches == []:
            new_nodes.append(node)
            continue


        str = node.text.split()
        first_del = "["
        second_del = ")"
        arr = []
        num_links = len(link_matches)
        count = 0
        beginning = True
        in_alt = False

        #iterates through words in sentence
        for s in str:
            #adds word to arr if doesnt begin or end with delimiters for links
            if s.startswith(first_del) == False and s.endswith(second_del) == False and in_alt == False:
                arr.append(s)
            elif s.startswith(first_del):
                in_alt = True
                #adds the leading text, adds a space only at end if beginning of sentence and one before and after if in middle
                if beginning == True and arr != []:
                    new_nodes.append(TextNode(" ".join(arr) + " ", TextType.TEXT))
                    beginning = False
                elif arr != []:
                    new_nodes.append(TextNode(" " + " ".join(arr) + " ", TextType.TEXT))
                
                #resets the array, adds the link text node to the new nodes and preps for next link
                arr = []
                new_nodes.append(TextNode(link_matches[count][0], TextType.LINK, link_matches[count][1]))
                count += 1

            first_del_count = s.count(first_del)
            while first_del_count > 0 and s.startswith(first_del) == False:
                new_nodes.append(TextNode(link_matches[count][0], TextType.LINK, link_matches[count][1]))
                count += 1
                first_del_count -= 1
            
            if s.endswith(second_del) == True:
                in_alt = False
        
        #adds text node w/ leading space if there are any more words in the text
        if arr != []:
            new_nodes.append(TextNode(" " +" ".join(arr), TextType.TEXT))


    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    tnode = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([tnode], '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes