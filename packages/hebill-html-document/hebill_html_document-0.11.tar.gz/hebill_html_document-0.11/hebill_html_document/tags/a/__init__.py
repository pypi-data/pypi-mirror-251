from hebill_html_document.nodes.tag import tag


class a(tag):
    output_break_inner = False

    def __init__(self, senior, title: str = None, url: str = None):
        super().__init__(senior)
        if title is not None:
            self.create().node().content(title)
        self.attributes["href"] = ""
        if url is not None:
            self.attributes["href"] = url

