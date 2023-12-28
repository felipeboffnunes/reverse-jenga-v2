from dash import html

from app.components.bento_cards import Grid, BentoCard
from app.layouts.fragments.menu import menu_fragment

home = Grid(
    [BentoCard(c, v, h) for c, v, h in [
        [html.H1("Reverse Jenga -v2", style={'textAlign': 'left', 'flex': '1'}), (1,1), (1, 2)],
        [menu_fragment, (1, 2), (1, 9)],
        [html.Div(id="main-page-content"), (2, 1), (10,10)],
    ]]
)
