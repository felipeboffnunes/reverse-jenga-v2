from dash import html, dcc, dash_table
import plotly.express as px
from app.components.delta_tracker import process_session_data
from app.utils.db import get_table_names


def _build(layout):
    df = process_session_data(16)
    fig = px.line(df, y='moving_avg', title='Moving Average of Time Taken to Read Each Page')
    #fig.update_layout(xaxis_title='Page Number', yaxis_title='Time (Minutes, Moving Average)')
    # Metrics Display
    # metrics_info = html.Div([
    #     html.P(f"Average Pages Per Day: {avg_pages_day:.2f}"),
    #     html.P(f"Total Pages Read: {total_read}"),
    #     html.P(f"Read to Total Pages Ratio: {total_ratio:.2%}"),
    #     html.P(f"Average Time Per Page: {avg_time_page:.2f} minutes")
    # ])
    layout["daily-reading-plot"].figure = fig
    #layout["metrics-info"].children = metrics_info
    return layout


session_layout = html.Div([
    html.H1("Database Tables"),
    dcc.Dropdown(
        id='table-dropdown',
        options=[{'label': name, 'value': value} for name, value in get_table_names()],
        placeholder="Select a table"
    ),
    dash_table.DataTable(id='session-table'),
    dcc.Graph(id='daily-reading-plot'),
    html.Div(id='metrics-info')
])

