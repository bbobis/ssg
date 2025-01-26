from typing import Any, Dict

from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(
        self, tag: str | None, value: str, props: Dict[str, Any] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        props = "test" if self.props_to_html() == "" else " "
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
