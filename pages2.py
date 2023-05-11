import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
from collections import OrderedDict
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path='/page-2', name='Container Deposit')

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = df[['continent', 'country', 'pop', 'lifeExp']]
dff = px.data.gapminder()

dfTips = px.data.tips()
fig = px.sunburst(dfTips, path=['day', 'time', 'sex'], values='total_bill')
fig1 = px.scatter(dff, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])


layout = dbc.Container([
    dcc.Markdown('# Interactive Container Deposit', style={'textAlign':'center'}),
    dbc.Row([
    	dbc.Col([
    		continent_drop := dcc.Dropdown([x for x in sorted(df.continent.unique())], placeholder='select continent')
    		], width=3),
    	dbc.Col([
    		country_drop := dcc.Dropdown([x for x in sorted(df.country.unique())], placeholder='select country')
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
    	]),
    dbc.Row([
		dbc.Col([
			dcc.Graph(figure=fig)
			], width={'size': 5}),
		dbc.Col([
			dcc.Graph(figure=fig1)
			],width={'size':7})
		])
    ])
    
@callback(
	Output(my_table, 'data'),
	Input(continent_drop, 'value'),
	Input(country_drop, 'value')
	)
def update_dash(value_ctn, value_cty):
	dff = df.copy()

	if value_ctn:
		dff = dff[dff.continent == value_ctn]
	if value_cty:
		dff = dff[dff.country == value_cty]

	return dff.to_dict('records')





