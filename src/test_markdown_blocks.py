import unittest

from markdown_blocks import (
  markdown_to_blocks
)

class TestTextNode(unittest.TestCase):
  def test_markdown_to_blocks(self):
    text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
    self.assertEqual(markdown_to_blocks(text), [
      "This is **bolded** paragraph",
      "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
      "* This is a list\n* with items"
    ])

  def test_markdown_to_blocks_many_newlines(self):
    text = """This is **bolded** paragraph

    

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line




* This is a list
* with items"""
    self.assertEqual(markdown_to_blocks(text), [
      "This is **bolded** paragraph",
      "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
      "* This is a list\n* with items"
    ])

  def test_markdown_to_blocks_only_space_lines(self):
    text = """Here's some text!
      
The last line has only spaces."""
    self.assertEqual(markdown_to_blocks(text), [
      "Here's some text!",
      "The last line has only spaces."
    ])

if __name__ == "__main__":
  unittest.main()
