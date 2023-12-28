import dash

from app.callbacks import register_callbacks
from app.layouts.home import home

app = register_callbacks(dash.Dash(__name__))

app.layout = home.generate()
