from ..figure import Figure
from plotly import graph_objects as go
from plotly.basedatatypes import BaseTraceType
from typing import Union, Optional
def wrap_div(html, class_=None):
    if class_:
        return f"<div class='{class_}'>\n{html}\n</div>\n"
    else:
        return f'<div>\n{html}\n</div>\n'

class GoFigure(Figure):
    """
    Class representing a plotly go figure in the report
    """
    def __init__(self, figure_data: Union[list[BaseTraceType], dict, go.Figure], caption:str, notes:Optional[list[str]] = None, post_script: str = ""):
        """
        The constructor of the GoFigure class
        Args:
            figure_data (dict|go.Figure): The figure data or the go.Figure object
            caption(str): The caption text
            notes (List[str]): The notes to be added to the caption
            post_script: javascript code to be executed after the figure is rendered
        """
        super(GoFigure, self).__init__(caption, notes)
        self.figure_data = figure_data
        self.post_script = post_script
        self.figure_obj = go.Figure(self.figure_data)

    def _as_html_figure_content(self):

        html = wrap_div(self.figure_obj.to_html(config={"displayModeBar": True},
                                                            # show_link=False,
                                                            include_plotlyjs=False,
                                                            # output_type='div',
                                                            full_html=False,
                                                            post_script=self.post_script),
                        class_='figure_div')

        return html
