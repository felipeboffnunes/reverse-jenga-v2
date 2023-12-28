import pandas as pd
from dash import html, Input, Output, State, dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from app.components.delta_tracker import process_session_data
from app.layouts.tower import books_layout
from app.layouts.session import session_layout
from app.utils.db import fetch_data, add_book, get_session_data
import plotly.express as px
def register_main_layout_callbacks(app):

    @app.callback(
        Output("main-page-content", "children"),
        Input("menu_fragment_tabs", "value")
    )
    def routes_tab(tab):
        return _routes_main_tab(tab)

    @app.callback(
        Output("daily-reading-plot", "figure"),
        [Input('table-dropdown', 'value')]
    )
    def update_table(selected_table):
        if selected_table is not None:
            df = process_session_data(selected_table)
            fig = go.Figure()
            book_data = fetch_data("book_info").to_dict('records')
            for i, book_id in enumerate(df['book_id'].unique()):
                df_book = df[df['book_id'] == book_id]
                book_name = book_data[book_id-1]['Title']
                fig.add_trace(go.Scatter(
                    x=df_book['page_end'],
                    y=df_book['moving_avg'],
                    mode='lines',
                    name='Moving Average',
                    line=dict(color="#00ADB5", width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=df_book['page_end'],
                    y=df['read_time'],
                    mode='markers',
                    name=book_name,
                    marker=dict(color="#F9F7F7", size=3),
                ))
                fig.add_trace(go.Scatter(
                    x=df['page_end'],
                    y=df['read_time'],
                    mode='lines',
                    name='Read Time',
                    line=dict(color='rgba(255, 255, 255, 0.5)', width=1),
                ))

            fig.update_layout(
                xaxis_title='Time',
                xaxis=dict(
                    type='date',
                    tickmode='linear',
                    tickformat='%H:%M',
                ),
                yaxis=dict(
                    showgrid=False,
                    showticklabels=False
                ),
                plot_bgcolor="#222831",
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),  # Reduce margins
                hovermode='closest',
            )

            return fig
        return dash.no_update

    @app.callback(
        Output('books-table', 'data'),
        [Input('add-book-button', 'n_clicks')],
        [State('title-input', 'value'), State('author-input', 'value'), State('pages-input', 'value')]
    )
    def add_new_book(n_clicks, title, author, pages):
        if n_clicks and title and author and pages:
            add_book(title, author, pages)
            return fetch_data("book_info").to_dict('records')
        return dash.no_update

    return app


def _routes_main_tab(tab: str = "DEFAULT") -> html.Div:
    tabs_layout = {
        "DEFAULT": html.Div(
            html.H3("Default Tab"),
        ),
        "TOWERS": html.Div(
            books_layout,
        ),
        "SESSION": html.Div(
            session_layout,
        ),
    }
    return tabs_layout[tab]


def register_callbacks(app):
    app = register_main_layout_callbacks(app)
    return app
