from  textnode import TextNode , TextType
from  htmlnode import HTMLNode
from leafnode import LeafNode

from utilities import text_to_textnodes

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

    nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    nodes2 = text_to_textnodes("**bold_italic_**code")
    print("HEJ")
    print(nodes)
    print(nodes2)

    node5 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(node5.to_html())

main()