import unittest
from htmlnode import HTMLNode




class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        html1 = HTMLNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        html2 = HTMLNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        self.assertEqual(html2, html1)

    def test_props_none(self):
        html1 = HTMLNode(tag="p", value="This is a paragraph.")
        html2 = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertEqual(html2, html1)

    def test_props_to_html(self):

        valid_result = ' class="text" title="oskar"'

        html1 = HTMLNode(tag="p", value="This is a paragraph.", props={"class": "text" , "title": "oskar"})
        result = HTMLNode.props_to_html(html1)
        self.assertEqual(valid_result, result)