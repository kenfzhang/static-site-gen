from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

import re

class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other) :
    return (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url)

  def __repr__(self):
    return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
  if text_node.text_type not in {"text", "bold", "italic",
                                 "code", "link", "image"}:
    raise Exception("Invalid text type")
  if text_node.text_type == "text":
    return LeafNode(None, text_node.text)
  if text_node.text_type == "bold":
    return LeafNode("b", text_node.text)
  if text_node.text_type == "italic":
    return LeafNode("i", text_node.text)
  if text_node.text_type == "code":
    return LeafNode("code", text_node.text)
  if text_node.text_type == "link":
    return LeafNode("a", text_node.text, {"href": text_node.url})
  if text_node.text_type == "image":
    return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
      
def has_opening_delimiter(text, delimiter):
  return (len(text) >= len(delimiter) and text[:len(delimiter)] == delimiter)
  
def has_closing_delimiter(text, delimiter):
  return (len(text) >= len(delimiter) and text[-len(delimiter):] == delimiter)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for n in old_nodes:
    n_parts = n.text.split()
    curr = ""
    i = 0

    # main loop
    while i < len(n_parts):
      if not has_opening_delimiter(n_parts[i], delimiter):
        curr += n_parts[i] + " "
      else:
        new_nodes.append(TextNode(curr, text_type_text, None))
        curr = ""
        curr += n_parts[i].lstrip(delimiter).rstrip(delimiter) + " "
        while not has_closing_delimiter(n_parts[i], delimiter):
          i += 1
          curr += n_parts[i].lstrip(delimiter).rstrip(delimiter) + " "
        new_nodes.append(TextNode(curr[:-1], text_type, None))
        curr = ""
      i += 1
    new_nodes.append(TextNode(" "+curr[:-1], text_type_text, None))    
  return new_nodes

# Functions for processing nodes with images and links

def extract_markdown_images(text):
  matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
  return matches

def extract_markdown_links(text):
  matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
  return matches

def is_markdown_image(text):
  return True if re.match(r"!\[(.*?)\]\((.*?)\)", text) else False

def is_markdown_link(text):
  return True if re.match(r"\[(.*?)\]\((.*?)\)", text) else False

def split_nodes_image(old_nodes):
  new_nodes = []
  for n in old_nodes:
    n_img = extract_markdown_images(n.text)
    if len(n_img) <= 0:
      new_nodes.append(n)
      continue
    # Node as a list of strings, separated where images are
    split_by_images = []
    img_split = n.text.split(f"![{n_img[0][0]}]({n_img[0][1]})")
    curr_split = img_split
    split_by_images.append(curr_split[0])
    split_by_images.append(f"![{n_img[0][0]}]({n_img[0][1]})")
    for i in range(1, len(n_img)):
      curr_split = curr_split[1].split(f"![{n_img[i][0]}]({n_img[i][1]})")
      split_by_images.append(curr_split[0])
      split_by_images.append(f"![{n_img[i][0]}]({n_img[i][1]})")
    if len(split_by_images[0]) == 0:
      split_by_images = split_by_images[1:]
    for s in split_by_images:
      # detect if each element is image or not.
      if is_markdown_image(s):
        new_nodes.append(
          TextNode(n_img[0][0], text_type_image, n_img[0][1])
        )
        n_img = n_img[1:]
      else:
        new_nodes.append(
          TextNode(s, text_type_text, None)
        )
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for n in old_nodes:
    n_link = extract_markdown_links(n.text)
    if len(n_link) <= 0:
      new_nodes.append(n)
      continue
    # Node as a list of strings, separated where links are
    split_by_links = []
    link_split = n.text.split(f"[{n_link[0][0]}]({n_link[0][1]})")
    curr_split = link_split
    split_by_links.append(curr_split[0])
    split_by_links.append(f"[{n_link[0][0]}]({n_link[0][1]})")
    for i in range(1, len(n_link)):
      curr_split = curr_split[1].split(f"[{n_link[i][0]}]({n_link[i][1]})")
      split_by_links.append(curr_split[0])
      split_by_links.append(f"[{n_link[i][0]}]({n_link[i][1]})")
    if len(split_by_links[0]) == 0:
      split_by_links = split_by_links[1:]
    for s in split_by_links:
      # detect if each element is link or not.
      if is_markdown_link(s):
        new_nodes.append(
          TextNode(n_link[0][0], text_type_link, n_link[0][1])
        )
        n_link = n_link[1:]
      else:
        new_nodes.append(
          TextNode(s, text_type_text, None)
        )
  return new_nodes