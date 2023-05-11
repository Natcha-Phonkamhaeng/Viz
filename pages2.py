import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
from collections import OrderedDict
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path='/page-2', name='Container Deposit')

df = px.data.tips()
fig = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')

dff = px.data.gapminder()
fig1 = px.scatter(dff, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])


data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(data)


layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dcc.Dropdown(["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"], id='dropdown-year', multi=True, placeholder='select city')
			], width={'size': 4}),
		dbc.Col([
			dcc.Dropdown(["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"], 
    		id='dropdown-month', multi=True, placeholder='select day')
			], width={'size':4}),
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			dash_table.DataTable(
				id='table-container',
			    data=df.to_dict('records'),
			    columns=[{'id': c, 'name': c} for c in df.columns],
			    style_as_list_view=True,
			    style_data={ 'border': '1px solid black' },
			    style_header={
			        'backgroundColor': '#f8f9fa',
			        'fontWeight': 'bold'
			    },
			    style_cell_conditional=[
			        {
			            'if': {'column_id': c},
			            'textAlign': 'left'
			        } for c in ['Date', 'Region']
			    ]
			)	
			], width={'size':11})
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

















