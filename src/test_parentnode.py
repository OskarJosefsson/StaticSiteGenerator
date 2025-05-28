import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )

    def test_is_children_empty(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
        parent_node.to_html(),
        "<div></div>")

    def test_multiple_parents_siblings(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node])
        self.assertEqual(parent_node1.to_html() + parent_node2.to_html(), "<div><span>child</span></div><div><span>child</span></div>")

    def test_multiple_parent_siblings(self):
        child_node = LeafNode("span", "child")
        parent_node2 = ParentNode("div", [child_node])
        parent_node3 = ParentNode("div", [child_node])
        parent_node1 = ParentNode("div", [parent_node2, parent_node3])

        self.assertEqual(parent_node1.to_html(), "<div><div><span>child</span></div><div><span>child</span></div></div>")



