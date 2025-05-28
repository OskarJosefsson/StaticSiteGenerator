class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop_list = []

        if not self.props:
           return ""
        
        for key,value in self.props.items():
            prop_list.append(f'{key}="{value}"')

        return(" " + " ".join(prop_list))
    
    def __eq__(self, other):

        if not isinstance(other, HTMLNode):
            return NotImplemented
        
        if (self.tag == other.tag 
            and self.value == other.value 
            and (self.children or []) == (other.children or []) 
            and (self.props or {}) == (other.props or {})):
            return True
        else: return False
    

    def __repr__(self):

        string_result = f"{self.tag}, {self.value}"

        prop_list = []
        if self.props != None:
            for key,value in self.props.items():
                prop_list.append(f'{key}="{value}"')
            string_result  = string_result + " " + f"props=[{"".join(prop_list)}]"

        children_list = []
        if self.children != None:
            for item in self.children:
                children_list.append(str(item))
            string_result  = string_result + " " +  f"children=[{" ".join(children_list)}]" 

        return string_result

    

