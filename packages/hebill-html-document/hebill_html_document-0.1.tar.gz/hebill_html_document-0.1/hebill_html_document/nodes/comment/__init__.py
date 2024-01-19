from __future__ import annotations

from hebill_html_document.nodes.node import node
from hebill_html_document import document
from hebill_html_document.nodes.group import group


class comment(node):
    def __init__(self, senior: document | group, text: str = None):
        super().__init__(senior)
        self.text: str = "" if text is None else text

    def output(self):
        import html
        s = ""
        if self.document.output_break:
            s += "\n" + self.document.output_retraction * self.level()
        s += f"<!--[{html.escape(self.text)}]-->"
        self.document.output_next_breakable = True
        return s
