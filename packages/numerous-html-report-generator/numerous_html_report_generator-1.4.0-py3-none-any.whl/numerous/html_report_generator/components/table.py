from ..block import Block
from typing import List
from ..caption import Caption


class Table(Block):
    """
    Class representing a table in the report
    This is not meant to be used directly but to be inherited by specific table classes
    """
    def __init__(self, caption:str, notes: List[str]):
        self.caption = Caption(caption=caption, notes=notes, type="Table")



    # Overwrite this function in specific figure class
    def as_html_figure_content(self):
        return ""

    def _as_html(self):
        return f"{self.as_html_figure_content()+self.caption.caption_as_html()}"

