from ..block import Block
from typing import Optional
from ..caption import Caption


class Figure(Block):
    """
    Class representing a figure in the report
    This is not meant to be used directly but to be inherited by specific figure classes
    """
    def __init__(self, caption:str, notes: Optional[list[str]] = None):
        """

        Args:
            caption (str): The caption text
            notes (List[str]): The notes to be added to the caption
        """
        self.caption = Caption(caption=caption, notes=notes, type="Figure")

    def _as_html_figure_content(self):
        return ""

    def _as_html(self):
        return f"{self._as_html_figure_content() + self.caption.caption_as_html()}"

