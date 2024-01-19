from hebill_html_document.nodes.tag import tag


class span(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, None)
        self.output_break_inner = False
        if text is not None:
            self.create().node().content(text)
