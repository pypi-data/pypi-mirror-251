from __future__ import annotations

from hebill_html_document.nodes.group import group


class tag(group):
    def __init__(self, senior, name: str = None):
        super().__init__(senior)
        if name is not None:
            self.name = name
        else:
            n = self.__class__.__name__
            if n[-1] == "_":
                n = n[:-1]
            n.replace("_", "_")
            self.name = n
        self.attributes: dict = {}
        self.output_breakable = True

    def output(self):
        s = ""
        if self.document.output_break:
            if self.output_breakable and self.document.output_next_breakable:
                if self.level() > 0:
                    s += "\n"
            s += self.document.output_retraction * self.level()
        s += "<" + self.name
        # s += self.Attributes().output()
        s += ">"
        self.document.output_next_breakable = True
        si = super().output()
        s += si
        if self.document.output_break:
            if si != "" and self.document.output_next_breakable:
                s += "\n" + "	" * self.level()
        s += "</" + self.name + ">"
        self.document.output_next_breakable = True
        return s
