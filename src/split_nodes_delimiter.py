from textnode import *

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
            pass
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
            pass
        elif first_del == True and second_del == False:
            raise Exception("invalid markdown syntax")
        elif first_del == False and second_del == True:
            new_nodes.append(node)
            pass
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
            mid = ' '.join(mid)
            mid_node = TextNode(mid, text_type)  
            new_nodes.append(mid_node)

            #if the ending index is the length of the string, then there is no need to create a text node for the end
            if ending_index + 1 != len(spl) and second_del:
                last = TextNode(" " + " ".join(spl[ending_index + 1:]), TextType.TEXT)
                new_nodes.append(last)
            
    return new_nodes  
        