from __future__ import annotations


class document:
    def __init__(self):
        self.elements = {}
        self.titles = []
        self.title_delimiter = " > "
        self.output_break = True
        self.output_retraction = "	"
        self.output_next_breakable = True
