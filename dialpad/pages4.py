import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-4', name='Dialpad', order=4)

magenta = '#db0f72'

df = pd.read_excel('data/dialpad.xlsx')

layout = dbc.Container([
	html.H1(['As of May 2023'], className='mb-3'),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.H3(['Missed Call'], style={'color':'red'}),
							dcc.Markdown(children=['''# 18'''], id='miss_number', style={'color': 'red'})
							])
						], 
						style={'text-align':'center'})
					], 
					class_name='shadow')
				], 
				class_name='mb-5')
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.H3(['Choose Call In']),
							dcc.Dropdown(options=[x for x in df['Call In'].unique()], id='dropdown_call')
							])
						])
					],
					class_name='shadow'
					)
				])
			])
		]),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(id='bar_chart')
					])
				],
				class_name='shadow'
				)
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(id='pie_chart')
					],
					class_name='shadow'
					)
				])
			])
		])
	])
	