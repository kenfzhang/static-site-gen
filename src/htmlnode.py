class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props={}):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    html = ""
    for i in self.props:
      html += f' {i}="{self.props[i]}"'
    return html

  def __repr__(self):
    return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props={}):
    super().__init__(tag, value, None, props)

  def __repr__(self):
    return f'LeafNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

  def to_html(self):
    if self.value is None:
      raise ValueError("LeafNode must have value")
    if self.tag is None:
      return self.value
    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props={}):
    super().__init__(tag, None, children, props)

  def __repr__(self):
    return f'ParentNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

  def to_html(self):
    if self.tag is None:
      raise ValueError("Tag must be provided")
    if self.children is None:
      raise ValueError("Children nodes are required")
    html = f'<{self.tag}{self.props_to_html()}>'
    for c in self.children:
      html += c.to_html()
    html += f'</{self.tag}>'
    return html