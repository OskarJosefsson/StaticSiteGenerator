import re
from textnode import TextNode, TextType 

def extract_markdown_images(text):
        pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
        matches = re.findall(pattern, text)
        return matches

def extract_markdown_links(text):
        pattern = r'(?<!!)\[([^\[\]]+)\]\(([^()\s]+)\)'
        return re.findall(pattern, text)
        
def extract_markdown_images_finditer(text):
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.finditer(pattern, text)
    return [
        {
            'text': m.group(1),
            'url': m.group(2),
            'start': m.start(),
            'end': m.end(),
            'kind': TextType.IMG
        }
        for m in matches
    ]

def extract_markdown_links_finditer(text):
    pattern = r'(?<!!)\[([^\[\]]+)\]\(([^()\s]+)\)'
    matches = re.finditer(pattern, text)
    return [
        {
            'text': m.group(1),
            'url': m.group(2),
            'start': m.start(),
            'end': m.end(),
            'kind': TextType.LINK
        }
        for m in matches
    ]

def extract_markdown_bold_finditer(text):
    pattern = r'\*\*(.+?)\*\*'
    matches = re.finditer(pattern, text)
    return [
        {
            'text': m.group(1),
            'url': None,
            'start': m.start(),
            'end': m.end(),
            'kind': TextType.BOLD
        }
        for m in matches
    ]

def extract_markdown_italic_finditer(text):
    pattern = r'_([^_]+)_'
    matches = re.finditer(pattern, text)
    return [
        {
            'text': m.group(1),
            'url': None,
            'start': m.start(),
            'end': m.end(),
            'kind': TextType.ITALIC
        }
        for m in matches
    ]

def extract_markdown_code_finditer(text):
    pattern = r'`(.+?)`'
    matches = re.finditer(pattern, text)
    return [
        {
            'text': m.group(1),
            'url': None,
            'start': m.start(),
            'end': m.end(),
            'kind': TextType.CODE
        }
        for m in matches
    ]
def split_nodes_image(old_nodes):
        list_of_nodes = []

        for on in old_nodes:
            new_text = on.text
            result = extract_markdown_images(new_text)

            if not result:
                    if new_text != "":
                        text_node = TextNode(new_text, TextType.TEXT)
                        list_of_nodes.append(text_node)
                        continue
            else :
                tpl = result[0]
                text = new_text.split(f"![{tpl[0]}]({tpl[1]})")
                if text[0] != "":
                    text_node = TextNode(text[0], TextType.TEXT)
                    list_of_nodes.append(text_node)
                node = TextNode(tpl[0], TextType.IMG, tpl[1])
                list_of_nodes.append(node)
                list_of_nodes.extend(split_nodes_image([TextNode(text[1], TextType.TEXT)]))
            
                continue
        return list_of_nodes


def split_nodes_link(old_nodes):
    list_of_nodes = []

    for on in old_nodes:
         new_text = on.text
         result = extract_markdown_links(new_text)

         if not result:
            if new_text != "":
                text_node = TextNode(new_text, TextType.TEXT)
                list_of_nodes.append(text_node)
                continue
         else:
              tpl = result[0]
              text = new_text.split(f"[{tpl[0]}]({tpl[1]})")
              if text[0] != "":
                    text_node = TextNode(text[0], TextType.TEXT)
                    list_of_nodes.append(text_node)
              node = TextNode(tpl[0], TextType.LINK, tpl[1])
              list_of_nodes.append(node)
              list_of_nodes.extend(split_nodes_link([TextNode(text[1], TextType.TEXT)]))
              continue

    return list_of_nodes




def text_to_textnodes (string_to_node):
    list_of_nodes = []
    last_end = 0

    dict_of_elements = extract_markdown_links_finditer(string_to_node)
    dict_of_elements.extend(extract_markdown_images_finditer(string_to_node))
    dict_of_elements.extend(extract_markdown_bold_finditer(string_to_node))
    dict_of_elements.extend(extract_markdown_italic_finditer(string_to_node))
    dict_of_elements.extend(extract_markdown_code_finditer(string_to_node))
    dict_of_elements = sorted(dict_of_elements, key=lambda x: x['start'])
    
    for item in dict_of_elements:
        if item["start"] > last_end:
              list_of_nodes.append(TextNode(string_to_node[last_end:item["start"]], TextType.TEXT))
              list_of_nodes.append(TextNode(item["text"], item["kind"], item["url"]))
        else :
            list_of_nodes.append(TextNode(item["text"], item["kind"], item["url"]))
        last_end = item["end"]

    if string_to_node[last_end:] != "":                 
        list_of_nodes.append(TextNode(string_to_node[last_end:], TextType.TEXT))



    return list_of_nodes     
         
                  
         
         
        
def split_nodes_delimiter (old_nodes, delimiter, text_type):
        list_of_nodes = []
        for on in old_nodes:
            new_text = on.text
            if on.text_type == TextType.TEXT:
                if new_text.count(delimiter) % 2 != 0:
                    raise ValueError("Not even amount of delimiters, cant parse")
                checker = False
                while len(new_text) > 0:
                        
                    index = new_text.find(delimiter)
                    if index == -1:
                            new_node = new_text
                            if checker is False:
                                list_of_nodes.append(TextNode(new_node, TextType.TEXT))
                            else:
                                list_of_nodes.append(TextNode(new_node, text_type))
                            break 
                    else:
                        new_node = ""
                        new_node = new_text[:index]
                        new_text = new_text[index + len(delimiter):]
                        if new_node == "":
                            continue
                        if checker is False:
                            list_of_nodes.append(TextNode(new_node, TextType.TEXT))
                            checker = True  
                        else:
                            list_of_nodes.append(TextNode(new_node, text_type))
                            checker = False 

            else: list_of_nodes.append(on)

        return list_of_nodes