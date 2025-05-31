from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "img"
    TEXT = "text"




class TextNode ():
    def __init__(self ,text, text_type, url=None):
        if not isinstance(text_type, TextType):
            raise ValueError("text_type must be an instance of TextType Enum")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
       if (self.text == other.text 
           and self.text_type == other.text_type 
           and self.url == other.url):
           return True
       else: return False

    def text_node_to_html_node(text_node):

        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)
            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text)
            case TextType.LINK:
                return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
            case TextType.IMG:
                return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        
        raise ValueError(f"No matching type found for {text_node.text_type}")

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
           
    


        
        
