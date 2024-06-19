import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("p", "Hey")
        self.assertEqual(node.__repr__(), "HTMLNode(tag=p, value=Hey, children=None, props={})")

    def test_props_to_html(self):
        node = HTMLNode("p", "Hey", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),f' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_print(self):
        node = LeafNode("p", "Hey", {})
        self.assertEqual(node.__repr__(), "LeafNode(tag=p, value=Hey, children=None, props={})")

    def test_props_to_html(self):
        node = LeafNode("a", "Link", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com" target="_blank">Link</a>')

class TestParentNode(unittest.TestCase):
    def test_children(self):
        node = ParentNode(
            "p",
            [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_nested(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Wow"),
                LeafNode("p", "Cool"),
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "One more layer")
                    ],
                    {"class": "dingus"}
                )
            ],
            {"class": "wingus"}
        )
        self.assertEqual(node.to_html(), '<div class="wingus"><p>Wow</p><p>Cool</p><div class="dingus"><p>One more layer</p></div></div>')