from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, text_type_text, text_type_code, text_type_bold

def main():
  node = TextNode("This is text with a `code block` word", text_type_text)
  new_nodes = split_nodes_delimiter([node], "`", text_type_code)
  print(new_nodes)

main()
