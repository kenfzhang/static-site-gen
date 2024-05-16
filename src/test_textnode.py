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
  extract_markdown_links
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

if __name__ == "__main__":
  unittest.main()
