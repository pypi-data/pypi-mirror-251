from __future__ import annotations
from hebill_html_document.nodes.tag import tag
from hebill_html_document.tags.body import body
from hebill_html_document.tags.head import head


class html(tag):
    def __init__(self, senior, lang: str = None):
        super().__init__(senior)
        if lang is not None:
            self.attributes["lang"] = lang
        self._junior_group_for_head = self.create().node().group()
        self._junior_tag_head: head | None = None
        self._junior_tag_body: body | None = None

    @property
    def junior_tag_head(self):
        if self._junior_tag_head is None:
            self._junior_tag_head = self._junior_group_for_head.create().tag().head()
        return self._junior_tag_head

    @property
    def junior_tag_body(self):
        if self._junior_tag_body is None:
            self._junior_tag_body = self.create().tag().body()
        return self._junior_tag_body
