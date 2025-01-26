from typing import Any, Dict, List

from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(
        self,
        tag: str | None,
        children: List["HTMLNode"] | None,
        props: Dict[str, Any] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children or len(self.children) == 0:
            raise ValueError("children is required")

        children_as_html = self.__children_to_html(self.children)
        props = self.props_to_html()
        props = props if props == "" else f" {props}"
        return f"<{self.tag}{props}>{children_as_html}</{self.tag}>"

    def __children_to_html(self, children: List["HTMLNode"]):
        if len(children) == 0:
            return ""
        result = self.__children_to_html(children[1:])
        return children[0].to_html() + result
