from bs4 import BeautifulSoup
from ..block import Block

class Section(Block):
    """
    Class representing a section in the report

    """

    def __init__(self,
                 section_title: str):
        """

        Args:
            section_title (str): The title of the section
        """
        self.section_title = section_title
        self.content = {}

    def set_content(self, content: dict):
        """
        Set the content of the section
        Args:
            content (dict): A dictionary of the content of the section, the keys are the titles of the blocks and the values are the blocks themselves

        Returns:

        """
        self.check_content(content)
        self.content = content

    def add_content(self, content: dict):
        """
        Add content to the section
        Args:
            content (dict): A dictionary of the content of the section, the keys are the titles of the blocks and the values are the blocks themselves

        Returns:

        """
        self.check_content(content)
        self.content.update(content)

    def check_content(self, content: dict):
        assert type(content) == dict
        #for block in content.values():
        #    assert isinstance(block, Block), f"Each item in the content should be a Block, this item has type {type(block)}"

    def _as_html(self):
        html = f"<div><h1 class=\"section_title editable\">{self.section_title}</h1></div>"
        for item in self.content.values():
            html += item._as_html()

        return html

class Subsection(Section):
    def _as_html(self):
        html = f"<div><h2 class=\"section_title editable\">{self.section_title}</h2></div>"
        for item in self.content.values():
            html += item._as_html()

        return html