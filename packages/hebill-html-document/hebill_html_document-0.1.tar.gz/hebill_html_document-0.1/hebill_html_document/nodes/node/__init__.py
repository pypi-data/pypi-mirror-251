from __future__ import annotations

from hebill_html_document.error import error


class node:
    def __init__(self, senior):
        # node cannot be instantiated directly. It must be inherited
        if type(self).__name__ == "Node":
            raise error(f"Class '{self.__class__.__name__}' cannot be instantiated directly. It must be inherited.")
        self.id = id(self)
        from hebill_html_document import document
        from hebill_html_document.nodes.group import group
        self.document: document
        self.senior: group | None = None
        if isinstance(senior, document):
            self.document = senior
        elif isinstance(senior, group):
            self.senior = senior
            self.document = senior.document
            self.senior.juniors[self.id] = self
        self.document.elements[self.id] = self
        self.output_breakable = False

    def level(self) -> int:
        if self.senior is None:
            return 0
        from hebill_html_document.nodes.group import group
        from hebill_html_document.nodes.tag import tag
        if isinstance(self, group) and not isinstance(self, tag):
            return self.senior.level()
        return self.senior.level() + 1

    def output(self) -> str:
        pass
