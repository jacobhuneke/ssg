import unittest

from extract import *

class TestHTMLNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_link(self):
        matches = extract_markdown_link(
            "This is text with an [link to youtube](https://www.youtube.com)"
        )        
        self.assertListEqual([("link to youtube", "https://www.youtube.com")], matches)     

    def test_two_links(self):
        matches = extract_markdown_link(
            "This is text with an [link to youtube](https://www.youtube.com) and a link [to google images](www.google.com/images)"
        )        
        self.assertListEqual([("link to youtube", "https://www.youtube.com"), ("to google images", "www.google.com/images")], matches)  

    def test_image_two_links(self):
        link_matches = extract_markdown_link(
            "This is text with an [link to youtube](https://www.youtube.com) and a link [to google images](www.google.com/images)" \
            "an image could be ![image of dog](https://dogimage.com/doggies)"
        )     
        image_matches = extract_markdown_images(
            "This is text with an [link to youtube](https://www.youtube.com) and a link [to google images](www.google.com/images)" \
            "an image could be ![image of dog](https://dogimage.com/doggies)"
        )
        self.assertEqual(image_matches, [('image of dog', 'https://dogimage.com/doggies')])
        self.assertEqual(link_matches, [('link to youtube', 'https://www.youtube.com'), ('to google images', 'www.google.com/images')])