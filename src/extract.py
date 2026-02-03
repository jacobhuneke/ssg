import re

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_link(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

