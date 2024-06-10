block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
  markdown = '\n'.join([m.strip() for m in markdown.split('\n')])
  markdown = markdown.split('\n\n')
  blocks = []
  for m in markdown:
    if len(m.strip()) > 0:
      blocks.append(m.strip('\n'))
  return blocks

def is_heading(block):
  pounds = 0
  for i in block:
    if pounds >= 1 and pounds <= 6 and i == ' ':
      return True
    if i == '#':
      pounds += 1
      continue
    else:
      return False
  return False

def is_code_block(block):
  return len(block) >= 6 and block[:3] == '```' and block[-3:] == '```'

def is_quote(block):
  block_lines = block.split('\n')
  for l in block_lines:
    if l[0] != '>':
      return False
  return True

def is_unordered_list(block):
  block_lines = block.split('\n')
  for l in block_lines:
    if l[:2] != '* ' and l[:2] != '- ':
      return False
  return True

def is_ordered_list(block):
  block_lines = block.split('\n')
  for i in range(len(block_lines)):
    if block_lines[i][:3] != str(i+1) + '. ':
      return False
  return True

def block_to_block_type(block):
  if is_heading(block):
    return block_type_heading
  if is_code_block(block):
    return block_type_code
  if is_quote(block):
    return block_type_quote
  if is_unordered_list(block):
    return block_type_unordered_list
  if is_ordered_list(block):
    return block_type_ordered_list
  return block_type_paragraph