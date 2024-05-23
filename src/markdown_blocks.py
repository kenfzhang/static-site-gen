def markdown_to_blocks(markdown):
  markdown = '\n'.join([m.strip() for m in markdown.split('\n')])
  markdown = markdown.split('\n\n')
  blocks = []
  for m in markdown:
    if len(m.strip()) > 0:
      blocks.append(m.strip('\n'))
  return blocks