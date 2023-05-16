import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import numpy as np


dash.register_page(__name__, path='/page-3', name='Icicle chart')

df = px.data.gapminder().query("year == 2007")
fig = px.icicle(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dcc.Markdown(['# Icicle chart template'], style={'textAlign':'center'})
			])
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			my_graph := dcc.Graph(figure=fig)
			], width=8),
		dbc.Col([
			html.Label('Continent', className='bg-primary text-white'),
			continent_drop := dcc.Dropdown([x for x in sorted(df.continent.unique())]),
			html.Label('Country', className='bg-primary text-white'),
			country_drop := dcc.Dropdown([x for x in sorted(df.country.unique())], multi=True),
			], width=4),
		]),
	dbc.Row([
		dbc.Col([
			my_table := dash_table.DataTable(
				data=df.to_dict('records'),
		        page_size=5,
		        sort_action='native',
				)
			])
		])
	])

@callback(
	Output(my_graph, 'figure'),
	Output(my_table, 'data'),
	Output(country_drop, 'options'),
	Input(continent_drop, 'value'),
	Input(country_drop, 'value')
	)
def update_graph(ctn_drop, select_country):
	dff = df.copy()

	if ctn_drop:
		dff = dff[dff.continent == ctn_drop]
		fig1 = px.icicle(dff, path=[px.Constant(ctn_drop), 'country'], values='pop',
		                  color='lifeExp', hover_data=['iso_alpha'],
		                  color_continuous_scale='RdBu',
		                  color_continuous_midpoint=np.average(dff['lifeExp'], weights=dff['pop']))
		fig1.update_layout(margin = dict(t=50, l=25, r=25, b=25))
		country = [x for x in sorted(dff['country'].unique())]

		if select_country is not None:
			dff = dff[dff.country.isin(select_country)]
			return fig, dff.to_dict('records'), country
		
		return fig1, dff.to_dict('records'), country
	
	else:
		return fig, df.to_dict('records'), [x for x in sorted(df['country'].unique())]		