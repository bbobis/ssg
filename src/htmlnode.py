from typing import Any, Dict, List


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, Any] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join(map(lambda item: f'{item[0]}="{item[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


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

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


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
