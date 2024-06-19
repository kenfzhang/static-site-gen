import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node.url, None)

    def test_not_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_image)
        self.assertNotEqual(node, node2)

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ])

    def test_split_delimiter_code_single_word(self):
        node = TextNode("This is text with a `code` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" word", text_type_text)
        ])

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold text** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold text", text_type_bold),
            TextNode(" word", text_type_text)
        ])

    def test_split_delimiter_multiple(self):
        node1 = TextNode("This is text with a *italic* word", text_type_text)
        node2 = TextNode("This is more text with some *italic* words", text_type_text)
        new_nodes = split_nodes_delimiter([node1, node2], "*", text_type_italic)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text),
            TextNode("This is more text with some ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" words", text_type_text)
        ])

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])

    def test_split_nodes_image_multiple(self):
        nodes = [
            TextNode("This node doesn't have any images", text_type_text),
            TextNode("But this one does! Look at it: ![image](https://avatars.githubusercontent.com/u/4808683?v=4)", text_type_text)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [
            TextNode("This node doesn't have any images", text_type_text),
            TextNode("But this one does! Look at it: ", text_type_text),
            TextNode("image", text_type_image, "https://avatars.githubusercontent.com/u/4808683?v=4"),
        ])

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                                        text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
        ])

    def test_split_nodes_link_multiple(self):
        nodes = [
            TextNode("This node doesn't have any links", text_type_text),
            TextNode("But this one does! Check it out: [link](https://example.com)", text_type_text)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, [
            TextNode("This node doesn't have any links", text_type_text),
            TextNode("But this one does! Check it out: ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
        ])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [
        TextNode("This is ", text_type_text),
        TextNode("text", text_type_bold),
        TextNode(" with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word and a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and a ", text_type_text),
        TextNode("link", text_type_link, "https://boot.dev"),
        ])

if __name__ == "__main__":
    unittest.main()
