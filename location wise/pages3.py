import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-3', name='Location Wise', order=3)

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
				dbc.Col([
					html.H2(['Choose Location'])
					])
				]),
			dbc.Row([
				dbc.Col([
					dcc.RadioItems(options=['BKK', 'LCB', 'SGZ'], value='BKK', inline=True, id='my_radio', labelStyle= {"margin":"1rem"}, style={'font-size':30})
					]),
				dbc.Col([
					dcc.Markdown(children='', id='my_location', style={'font-size': 35, 'color':'blue'})
					])
				]),
			html.Hr(),
			dbc.Row([
				dbc.Col([
					html.P(['Comparison']),
					dcc.Dropdown(options=['By Receipt Type', 'By Month', 'By Accumulative'], placeholder='By Receipt Type',id='my_dropdown'),
					html.Hr(),
					html.P(['Note:']),
					dcc.Markdown(children='', id='my_note'),
					], width=3),
				dbc.Col([
					dcc.Graph(figure={}, id='top_graph', className='mb-3'),
					dcc.Graph(figure={}, id='bottom_graph')
					], width=9)	
				])	
			])
		], class_name='shadow', style={'color': 'black'})
	])


# callback for header location
@callback(
	Output('my_location', 'children'),
	Input('my_radio', 'value')
	)
def update_location(select_location):
	if select_location == 'BKK':
		return ['BANGKOK']
	elif select_location == 'LCB':
		return ['LAEM CHABANG']
	else:
		return ['SONGKHLA']

# callback for update graph
@callback(
	Output('top_graph', 'figure'),
	Output('bottom_graph', 'figure'),
	Output('my_note', 'children'),
	Input('my_location', 'children'),
	Input('my_dropdown', 'value'),
	)
def update_graph(select_location, select_type):
	dff22 = df22.copy()
	dff23 = df23.copy()

	df = pd.concat([dff22, dff23])

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

	# 1) BKK Location
	if select_location == ['BANGKOK']:
		if select_type == 'By Month':
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
		elif select_type == 'By Accumulative':
			dfBkkHsbc = dfBkkHsbc.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
			dfBkkHsbc['Accu'] = dfBkkHsbc.groupby('Year').cumsum(numeric_only=True)

			figHsbc = go.Figure()
			figHsbc = figHsbc.add_trace(go.Scatter(x=dfBkkHsbc['Month'].unique().tolist(), y=dfBkkHsbc[dfBkkHsbc['Year'] == 2022]['Accu'].tolist(), name='FY22',fill='tozeroy'))
			figHsbc = figHsbc.add_trace(go.Scatter(x=dfBkkHsbc['Month'].unique().tolist(), y=dfBkkHsbc[dfBkkHsbc['Year'] == 2023]['Accu'].tolist(), name='FY23',fill='tozeroy'))
			figHsbc.update_layout(title={'text': 'HSBC', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)', 
						plot_bgcolor="rgba(0,0,0,0)")

			dfBkkBay = dfBkkBay.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
			dfBkkBay['Accu'] = dfBkkBay.groupby('Year').cumsum(numeric_only=True)

			figBay = go.Figure()
			figBay = figBay.add_trace(go.Scatter(x=dfBkkBay['Month'].unique().tolist(), y=dfBkkBay[dfBkkBay['Year'] == 2022]['Accu'].tolist(), name='FY22',fill='tozeroy'))
			figBay = figBay.add_trace(go.Scatter(x=dfBkkBay['Month'].unique().tolist(), y=dfBkkBay[dfBkkBay['Year'] == 2023]['Accu'].tolist(), name='FY23',fill='tozeroy'))
			figBay.update_layout(title={'text': 'Bay', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)', 
						plot_bgcolor="rgba(0,0,0,0)")
			return figHsbc, figBay, note
		else: # use default "By Receipt Type"
			return figHsbc, figBay, note

	else:
			return figHsbc, figBay, note
	
