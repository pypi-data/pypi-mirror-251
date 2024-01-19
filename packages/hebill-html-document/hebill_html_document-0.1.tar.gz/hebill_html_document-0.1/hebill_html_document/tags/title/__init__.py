from hebill_html_document.nodes.content import content
from hebill_html_document.nodes.tag import tag


class title(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, None)
        self.output_break_inner = False
        self.junior_content: content = self.create().node().content()
        if text is not None:
            self.junior_content.text = text
