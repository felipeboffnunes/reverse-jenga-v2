from dash import html, dash_table, dcc

from app.utils.db import fetch_data

books_layout = html.Div([
    html.H1("Books Information"),
    html.Div([
    html.Div([
        dcc.Input(id='title-input', type='text', placeholder='Title'),
        dcc.Input(id='author-input', type='text', placeholder='Author'),
        dcc.Input(id='pages-input', type='number', placeholder='Pages'),
        html.Button('Add Book', id='add-book-button')
    ]),
    dash_table.DataTable(id='books-table',
                         columns=[{"name": i, "id": i} for i in fetch_data("book_info").reset_index().columns],
                 data=fetch_data("book_info").reset_index().to_dict('records'),
                         )

])

])
