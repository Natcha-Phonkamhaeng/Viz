import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "10rem",
    #"margin-right": '5rem',
    #'padding': '2rem'
    #'margin-right': '10%',
    "margin-top": "2em"
}

sidebar = html.Div([
    html.Img(src='assets/logo.png'),
    html.Div(['Created By', html.Br(),'Natcha Phonkamhaeng'], style={'height': '1px', 'font-size':'15px'}),
    html.Br(),
    html.Br(),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink([
            html.Div(page['name'], className='ms-2')
            ],
            href=page['path'],
            active='exact',
            )
            for page in dash.page_registry.values()
        ], 
        vertical=True, pills=True),
    ])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            sidebar
            ],
            style=SIDEBAR_STYLE),
        dbc.Col([
            dash.page_container
            ],
            style=CONTENT_STYLE, width={'size':11})
        ])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
































