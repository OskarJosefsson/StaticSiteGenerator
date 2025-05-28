from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag,  children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Children is required")
        html = ""
        for element in self.children:
         html += element.to_html() 

        full_string = f"<{self.tag}>{html}</{self.tag}>"
        return full_string

    