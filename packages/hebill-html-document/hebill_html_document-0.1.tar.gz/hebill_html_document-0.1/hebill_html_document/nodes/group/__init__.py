from __future__ import annotations

from hebill_html_document.nodes.node import node


class group(node):
    def __init__(self, senior):
        super().__init__(senior)
        self.juniors: dict = {}
        self._create: group_create_function_object | None = None

    def create(self):
        if self._create is None:
            self._create = group_create_function_object(self)
        return self._create

    def output(self):
        s = ""
        if len(self.juniors) > 0:
            for key, value in self.juniors.items():
                from hebill_html_document.nodes.node import node
                if isinstance(value, node):
                    s += value.output()
        return s


class group_create_function_object:
    def __init__(self, senior):
        self.senior = senior
        self._node: group_create_node_function_object | None = None
        self._tag: group_create_tag_function_object | None = None

    def node(self) -> group_create_node_function_object:
        if self._node is None:
            self._node = group_create_node_function_object(self.senior)
        return self._node

    def tag(self) -> group_create_tag_function_object:
        if self._tag is None:
            self._tag = group_create_tag_function_object(self.senior)
        return self._tag


class group_create_node_function_object:
    def __init__(self, senior):
        self.senior = senior

    def code(self, text: str = None):
        from hebill_html_document.nodes.code import code
        return code(self.senior, text)

    def content(self, text: str = None):
        from hebill_html_document.nodes.content import content
        return content(self.senior, text)

    def comment(self, text: str = None):
        from hebill_html_document.nodes.comment import comment
        return comment(self.senior, text)

    def group(self):
        return group(self.senior)

    def tag(self, name: str):
        from hebill_html_document.nodes.tag import tag
        return tag(self.senior, name)


class group_create_tag_function_object:
    def __init__(self, senior):
        self.senior = senior

    def a(self, title: str = None, url: str = None):
        from hebill_html_document.tags.a import a
        return a(self.senior, title, url)

    def body(self):
        from hebill_html_document.tags.body import body
        return body(self.senior)

    def div(self, content: str = None):
        from hebill_html_document.tags.div import div
        return div(self.senior, content)

    def head(self):
        from hebill_html_document.tags.head import head
        return head(self.senior)

    def html(self, lang: str = None):
        from hebill_html_document.tags.html import html
        return html(self.senior, lang)

    def input_text(self, name: str = None, value: str | int | float = None, placeholder: str = None):
        from hebill_html_document.tags.input_text import input_text
        return input_text(self.senior, name, value, placeholder)

    def link(self, url: str = None):
        from hebill_html_document.tags.link import link
        return link(self.senior, url)

    def span(self, text: str = None):
        from hebill_html_document.tags.span import span
        return span(self.senior, text)

    def title(self, text: str = None):
        from hebill_html_document.tags.title import title
        return title(self.senior, text)
