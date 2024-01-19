from __future__ import annotations

from hebill_html_document.nodes.tag import tag
from hebill_html_document.nodes.group import group
from hebill_html_document.tags.title import title


class head(tag):
    def __init__(self, senior):
        super().__init__(senior)
        self._junior_group_for_metas: group = self.create().node().group()
        self._junior_group_for_libraries: group = self.create().node().group()
        self._junior_tag_title: title | None = None

    @property
    def junior_tag_title(self):
        if self._junior_tag_title is None:
            self._junior_tag_title = self.create().tag().title()
        return self._junior_tag_title


