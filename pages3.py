import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
from collections import OrderedDict
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path='/page-3', name='Interactive Table', suppress_callback_exceptions=True)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = df[['continent', 'country', 'pop', 'lifeExp']]

layout = dbc.Container([
    dcc.Markdown('# Interactive data table', style={'textAlign':'center'}),
    dbc.Row([
    	dbc.Col([
    		continent_drop := dcc.Dropdown([x for x in sorted(df.continent.unique())], placeholder='select continent')
    		], width=3)
    	]),
    html.Br(),
    dbc.Row([
    	dbc.Col([
    		my_table := dash_table.DataTable(
    			columns=[
		            {'name': 'Continent', 'id': 'continent', 'type': 'text'},
		            {'name': 'Country', 'id': 'country', 'type': 'text'},
		            {'name': 'Population', 'id': 'pop', 'type': 'numeric'},
		            {'name': 'Life Expectancy', 'id': 'lifeExp', 'type': 'numeric'}
		        ],
		        data=df.to_dict('records'),
		        page_size=5,
		        filter_action='native'
    			)
    		])
    	])
    ])
    
@callback(
	Output(my_table, 'data'),
	Input(continent_drop, 'value')
	)
def update_dash(value):
	dff = df.copy()

	if value:
		dff = dff[dff.continent == value]

	return dff.to_dict('records')






