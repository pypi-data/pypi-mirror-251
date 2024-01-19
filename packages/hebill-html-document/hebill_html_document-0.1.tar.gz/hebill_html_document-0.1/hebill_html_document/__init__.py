from __future__ import annotations
from hebill_html_document.nodes.group import group_create_function_object


class document:

    def __init__(self):
        self.elements: dict = {}
        self.titles: list = []
        self.title_delimiter: str = " > "
        self.output_break: bool = True
        self.output_retraction: str = "	"
        self.output_next_breakable: bool = True
        # 设定默认html标签
        from hebill_html_document.tags.html import html
        self.root_tag_html: html = html(self)
        self._create: group_create_function_object | None = None

    def create(self) -> group_create_function_object:
        if self._create is None:
            self._create = group_create_function_object(self)
        return self._create

    def output(self) -> str:
        if len(self.titles) > 0:
            self.root_tag_html.junior_tag_head.junior_title.text.content = self.title_delimiter.join(self.titles)
        s = "<!DOCTYPE html>"
        if self.output_break:
            s += "\n"
        s += self.root_tag_html.output()
        return s


