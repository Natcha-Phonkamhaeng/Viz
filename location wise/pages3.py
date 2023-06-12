import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-3', name='AR Collection', order=3)

magenta = '#db0f72'

def change_df(dataframe, location, bank):
  mask = (dataframe['Office'] == location) & (dataframe['Bank Account'] == bank)
  return dataframe[mask]

df22 = pd.read_csv('data/Location Wise 22.csv')
df23 = pd.read_csv('data/Location Wise 23.csv')

layout = dbc.Container([
	dbc.Card([
		dbc.CardBody([
			dbc.Row([
				html.H2(['BANGKOK'])
				]),
			html.Hr(),
			dbc.Row([
				dbc.Col([
					html.P(['Comparison']),
					dcc.Dropdown(options=['By Receipt Type', 'By Month', 'By Accumulative'], placeholder='By Receipt Type',id='bkk_type'),
					html.Hr(),
					html.P(['Note:']),
					dcc.Markdown(children='', id='my_note'),
					], width=3),
				dbc.Col([
					dcc.Graph(figure={}, id='bkk_graph_hsbc', className='mb-3'),
					dcc.Graph(figure={}, id='bkk_graph_bay')
					], width=9)	
				])	
			])
		], class_name='shadow', style={'color': 'black'})
	])

# callback for Bkk location
@callback(
	Output('bkk_graph_hsbc', 'figure'),
	Output('bkk_graph_bay', 'figure'),
	Output('my_note', 'children'),
	Input('bkk_type', 'value'),
	)
def update_bkk_graph(select_type):
	dfBkk22 = df22.copy()
	dfBkk23 = df23.copy()

	df = pd.concat([dfBkk22, dfBkk23])

	dfBkkHsbc = change_df(df, 'BKKBB', 'HSBC')
	dfBkkBay = change_df(df, 'BKKBB', 'BAY')

	dfBkkHsbcRct = dfBkkHsbc.groupby(['Receipt Type', 'Bank Account', 'Year'])[['Total Amount']].agg('sum').reset_index()
	dfBkkBayRct = dfBkkBay.groupby(['Receipt Type', 'Bank Account', 'Year'])[['Total Amount']].agg('sum').reset_index()
	
	#---------------------------- default graph when user select "By Receipt Type"----------------------------
	figHsbc = px.histogram(dfBkkHsbcRct, x='Receipt Type', y='Total Amount', color='Year', barmode='group')
	figHsbc.update_layout(title={'text': 'HSBC', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

	figBay = px.histogram(dfBkkBayRct, x='Receipt Type', y='Total Amount', color='Year', barmode='group')
	figBay.update_layout(title={'text': 'BAY', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

	note = ['The amount shown is accumulative of Apr-May']
	
	if select_type == 'By Receipt Type':
		return figHsbc, figBay, note
	elif select_type == 'By Month':
		dfBkkHsbc = dfBkkHsbc.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
		dfBkkBay = dfBkkBay.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()

		figHsbc = px.histogram(dfBkkHsbc, x='Month', y='Total Amount', color='Year', barmode='group')
		figHsbc.update_layout(title={'text': 'HSBC', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")


		figBay = px.histogram(dfBkkBay, x='Month', y='Total Amount', color='Year', barmode='group')
		figBay.update_layout(title={'text': 'BAY', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

		return figHsbc, figBay, ['']


	else:
		return figHsbc, figBay, note
	
