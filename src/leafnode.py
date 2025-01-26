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
        props = self.props_to_html()
        props = props if props == "" else f" {props}"
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
