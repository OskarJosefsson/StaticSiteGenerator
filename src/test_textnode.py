import unittest
from textnode import TextNode, TextType 
import utilities

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_type_noneq(self):
        node = TextNode("This is a text node", TextType.IMG)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com/")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_img(self):
        node = TextNode("", TextType.IMG, url="test")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "test", "alt": ""})

    def test_img_with_alt(self):
        node = TextNode("alt text here", TextType.IMG, url="test")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "test", "alt": "alt text here"})

    def test_not_valid_type(self):
        with self.assertRaises(ValueError) as context:
            TextNode("hello", "not_a_text_type") 

        self.assertEqual(
            str(context.exception),
            "text_type must be an instance of TextType Enum"
        )

    def test_valid_text_type_succeeds(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertEqual(node.text, "hello")
        self.assertEqual(node.text_type, TextType.TEXT)


    def test_split_nodes_delimiter_even_bold(self):
       node = TextNode("hello **world** by oskar", TextType.TEXT)
       result = utilities.split_nodes_delimiter([node], "**", TextType.BOLD)
       expected_result = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.BOLD), TextNode(" by oskar", TextType.TEXT)]

       self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_even_italic(self):
       node = TextNode("hello **world** by oskar", TextType.TEXT)
       result = utilities.split_nodes_delimiter([node], "*", TextType.ITALIC)
       expected_result = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.ITALIC), TextNode(" by oskar", TextType.TEXT)]

       self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_odd_bold(self):
        node = TextNode("hello *world by oskar", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            utilities.split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "Not even amount of delimiters, cant parse")
    
    def test_extract_markdown_images(self):
        matches = utilities.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_two(self):
        matches = utilities.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) This is a second text with another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = utilities.extract_markdown_links(
            "This is text with an [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_two(self):
        matches = utilities.extract_markdown_links(
            "This is text with an [to boot dev](https://www.boot.dev), This is another text with an [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to boot dev", "https://www.boot.dev")], matches)


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    def test_split_links(self):
        node = TextNode(
        "This is text with an [to boot dev](https://www.boot.dev) and another [to boot dev2](https://www.boot.dev2)",
        TextType.TEXT,
        )
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "to boot dev2", TextType.LINK, "https://www.boot.dev2"
            ),
        ],
        new_nodes,
    )
        
    def test_single_link_only(self):
        node = TextNode("[OpenAI](https://openai.com)", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [TextNode("OpenAI", TextType.LINK, "https://openai.com")],
        new_nodes
    )
        


    def test_text_before_and_after_link(self):
        node = TextNode("Start [link](url.com) end", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("Start ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" end", TextType.TEXT),
        ],
        new_nodes
    )
        

    def test_multiple_links_no_spaces(self):
        node = TextNode("[a](1.com)[b](2.com)", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("a", TextType.LINK, "1.com"),
            TextNode("b", TextType.LINK, "2.com"),
        ],
        new_nodes
    )
        

    def test_no_links(self):
        node = TextNode("Just some text.", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [TextNode("Just some text.", TextType.TEXT)],
        new_nodes
    )
        
    def test_invalid_nested_link(self):
        node = TextNode("This is [a [nested] link](url.com)", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])

        self.assertListEqual(
        [TextNode("This is [a [nested] link](url.com)", TextType.TEXT)],
        new_nodes
    )
        
    def test_malformed_link(self):
        node = TextNode("This is [broken](link", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [TextNode("This is [broken](link", TextType.TEXT)],
        new_nodes
    )
        
    def test_single_image(self):
        node = TextNode("This is an image ![cat](cat.jpg)", TextType.TEXT)
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("cat", TextType.IMG, "cat.jpg"),
        ],
        new_nodes
    )

    def test_multiple_images(self):
        node = TextNode("Look ![a](a.jpg) and ![b](b.png)", TextType.TEXT)
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("Look ", TextType.TEXT),
            TextNode("a", TextType.IMG, "a.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.IMG, "b.png"),
        ],
        new_nodes
    )
        

    def test_image_start_and_end(self):
        node = TextNode("![start](s.png) middle ![end](e.png)", TextType.TEXT)
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("start", TextType.IMG, "s.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.IMG, "e.png"),
        ],
        new_nodes
    )
        
    def test_only_image(self):
        node = TextNode("![alt](image.png)", TextType.TEXT)
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [TextNode("alt", TextType.IMG, "image.png")],
        new_nodes
    )

    def test_consecutive_images(self):
        node = TextNode("![one](1.jpg)![two](2.jpg)", TextType.TEXT)
        new_nodes = utilities.split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("one", TextType.IMG, "1.jpg"),
            TextNode("two", TextType.IMG, "2.jpg"),
        ],
        new_nodes
    )
    
    def test_with_no_links(self):
        node = TextNode(
        "There are no links in this text",
        TextType.TEXT,
        )

        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("There are no links in this text", TextType.TEXT),
        ],
        new_nodes
    )

    def test_multiple_links_with_text_in_between(self):
        node = TextNode(
        "First [link1](url1), then some text, then [link2](url2).",
        TextType.TEXT,
        )
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(", then some text, then ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(".", TextType.TEXT),
        ],
        new_nodes
    )
        

    def test_multiple_links_with_text_in_between_3(self):
        node = TextNode(
        "First [link1](url1), with a link in between two [link2](url2) then some text, then [link3](url3).",
        TextType.TEXT,
        )
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(", with a link in between two ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" then some text, then ", TextType.TEXT),
            TextNode("link3", TextType.LINK, "url3"),
            TextNode(".", TextType.TEXT),
        ],
        new_nodes
    )
    def test_consecutive_links(self):
        node = TextNode("[one](1.com)[two](2.com)", TextType.TEXT)
        new_nodes = utilities.split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("one", TextType.LINK, "1.com"),
            TextNode("two", TextType.LINK, "2.com"),
        ],
        new_nodes
    )
        
if __name__ == "__main__":
    unittest.main()