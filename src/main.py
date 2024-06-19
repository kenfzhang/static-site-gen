from textnode import TextNode
from copystatic import copy_dir_contents

def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

    copy_dir_contents('./static/', './public/')

main()