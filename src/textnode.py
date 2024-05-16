from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

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