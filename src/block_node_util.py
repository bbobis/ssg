def markdown_to_block(markdown: str):
    blocks = []
    for block in markdown.split("\n\n"):
        blocks.append("\n".join(map(lambda s: s.strip(), block.strip().split("\n"))))
    return blocks
