from  textnode import TextNode , TextType
from  htmlnode import HTMLNode
from leafnode import LeafNode

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())
    html1 = HTMLNode(tag="p", value="This is a paragraph.", props={"class": "text" , "title": "oskar"})
    html2 = HTMLNode(tag="p", value="This is a paragraph.")
    html3 = HTMLNode(tag="p", value="This is a paragraph.", children=["li1", "li2", "li3"])

    print(html1.__repr__())
    print(html2.__repr__())
    print(html3.__repr__())
    print(html1.props_to_html())


    node5 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(node5.to_html())

main()