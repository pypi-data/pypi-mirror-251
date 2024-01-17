from numerous.html_report_generator.block import Block


class Div(Block):
    """
        Class representing a div in the report
    """
    def __init__(self, html:str, **kwargs):
        """

        Args:
            html: The html content of the div
            **kwargs:
        """
        self.html = html
        self.kwargs = kwargs

    def _as_html(self):
        modifiers=[]

        for k, v in self.kwargs.items():
            modifiers.append(f'{k}="{v}"')

        return f"<div {' '.join(modifiers)}>{self.html}</div>"
