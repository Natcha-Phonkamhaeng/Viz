import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-3', name='AR Collection', order=3)

magenta = '#db0f72'

def change_df(dataframe, location,bank):
  mask = (dataframe['Office'] == location) & (dataframe['Bank Account'] == bank)
  return dataframe[mask]

df22 = pd.read_csv('data/Location Wise 22.csv')
df23 = pd.read_csv('data/Location Wise 23.csv')

layout = dbc.Container([
	dbc.Card([
		dbc.CardBody([
			dbc.Row([
				html.H2(['BKK'])
				]),
			html.Hr(style={'color': 'black', "borderWidth": "0.3vh"}),
			dbc.Row([
				dbc.Col([
					html.P(['Year']),
					dcc.Dropdown(options=[2022, 2023], id='bkk_year'),
					html.P(['Receipt Type'], className='mt-3'),
					dcc.Dropdown(options=[x for x in df23['Receipt Type'].unique()], id='bkk_type', )
					], width=2),
				dbc.Col([
					dcc.Graph(figure={}, id='bkk_graph_hsbc', className='mb-3'),
					dcc.Graph(figure={}, id='bkk_graph_bay')
				],width=10)
				])
			])
		], class_name='shadow', style={'background-color': 'rgb(211,211,211)', 'color':'black'})
	])


# create callback for BKK
@callback(
	Output('bkk_graph_hsbc', 'figure'),
	Output('bkk_graph_bay', 'figure'),
	Input('bkk_year', 'value'),
	Input('bkk_type', 'value')
	)
def update_bkk(select_year, select_type):
	dfBkk22 = df22.copy()
	dfBkk23 = df23.copy()

	dfHsbc22 = change_df(dfBkk22, 'BKKBB','HSBC')
	dfHsbc23 = change_df(dfBkk23, 'BKKBB','HSBC')

	dfBay22 = change_df(dfBkk22, 'BKKBB','BAY')
	dfBay23 = change_df(dfBkk23, 'BKKBB','BAY')

	figHsbc = go.Figure(data=[
		go.Bar(name='FY22', 
			x=dfHsbc22.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Receipt Type'].tolist(), 
			y=dfHsbc22.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Total Amount'].tolist()),
		go.Bar(name='FY23', 
			x=dfHsbc23.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Receipt Type'].tolist(), 
			y=dfHsbc23.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Total Amount'].tolist())
		])
	figHsbc.update_layout(title={'text':'HSBC', 'x': 0.5},barmode='group', paper_bgcolor='rgb(176,196,222)', plot_bgcolor="rgba(0,0,0,0)", font_color='black')

	figBay = go.Figure(data=[
		go.Bar(name='FY22', 
			x=dfBay22.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Receipt Type'].tolist(), 
			y=dfBay22.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Total Amount'].tolist()),
		go.Bar(name='FY23', 
			x=dfBay23.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Receipt Type'].tolist(), 
			y=dfBay23.groupby(['Receipt Type'])[['Total Amount']].sum().reset_index()['Total Amount'].tolist())
		])
	figBay.update_layout(title={'text':'BAY', 'x': 0.5},barmode='group', paper_bgcolor='rgb(176,196,222)', plot_bgcolor="rgba(0,0,0,0)", font_color='black')

	if select_year:
		dfHsbc = pd.concat([dfHsbc22, dfHsbc23])
		dfHsbc = dfHsbc.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
		figHsbc = px.line(dfHsbc[dfHsbc['Year'] == select_year], x='Month', y='Total Amount', color='Year', markers=True)
		figHsbc.update_layout(title={'text':'HSBC: Comparison by Month', 'x': 0.5},barmode='group', paper_bgcolor='rgb(176,196,222)', plot_bgcolor="rgba(0,0,0,0)", font_color='black')

		dfBay = pd.concat([dfBay22, dfBay23])
		dfBay = dfBay.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
		figBay = px.line(dfBay[dfBay['Year'] == select_year], x='Month', y='Total Amount', color='Year', markers=True)
		figBay.update_layout(title={'text':'BAY: Comparison by Month', 'x': 0.5},barmode='group', paper_bgcolor='rgb(176,196,222)', plot_bgcolor="rgba(0,0,0,0)", font_color='black')

		return figHsbc, figBay
	else:
		return figHsbc, figBay
