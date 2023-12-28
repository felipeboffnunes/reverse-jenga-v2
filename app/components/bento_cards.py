from dash import html


class BentoCard:
    def __init__(self, content, top_left, bottom_right):
        """
        Initializes a BentoCard with given content and grid coordinates.

        Parameters:
        content: The Dash component or HTML content to display in the card.
        top_left (tuple): The (row, column) coordinates of the top-left corner.
        bottom_right (tuple): The (row, column) coordinates of the bottom-right corner.
        """
        self.content = content
        self.grid_row_start, self.grid_col_start = top_left
        self.grid_row_end, self.grid_col_end = bottom_right

    def generate(self):
        return html.Div(
            self.content,
            className="bento-card",
            style={
                'gridRowStart': self.grid_row_start,
                'gridRowEnd': self.grid_row_end,
                'gridColumnStart': self.grid_col_start,
                'gridColumnEnd': self.grid_col_end,
                'border': '1px solid #ddd',
                'padding': '20px',
                'margin': '10px',
                'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
            }
        )


class Grid:
    def __init__(self, content):
        self.content = content

    def generate(self):
        return html.Div(
            [card.generate() for card in self.content],
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(8, 1fr)',
                'gridGap': '10px',
                'padding': '10px'
            }
        )
