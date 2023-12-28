from dash import dcc

menu_fragment = dcc.Tabs(id="menu_fragment_tabs", value="DEFAULT", children=[
        dcc.Tab(label="Towers", value="TOWERS"),
        dcc.Tab(label="Session", value="SESSION"),
        dcc.Tab(label="About", value="DEFAULT"),
    ])
