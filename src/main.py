from textnode import *

def main():
    tn = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    tt = TextNode("This is some anchor text", TextType.IMAGE_TEXT)
    print(tn.__eq__(tt))

    print(tt.__repr__())




main()