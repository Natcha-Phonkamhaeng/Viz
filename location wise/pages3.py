import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-3', name='AR Collection', order=3)

magenta = '#db0f72'

def change_df(dataframe, bank):
  mask = (dataframe['Office'] == 'BKKBB') & (dataframe['Bank Account'] == bank)
  return dataframe[mask]

# df = px.data.gapminder().query("continent=='Oceania'")
# fig = px.line(df, x="year", y="lifeExp", color='country', title='Bank Name')
# # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",font_color = 'black')
# fig.update_layout(paper_bgcolor='rgb(176,196,222)', plot_bgcolor="rgba(0,0,0,0)", font_color='black')

df22 = pd.read_csv('data/Location Wise 22.csv')
df23 = pd.read_csv('data/Location Wise 23.csv')



layout = dbc.Container([
	dbc.Card([
		dbc.CardBody([
			dbc.Row([
				html.H2(['BKK'])
				]),
			html.Hr(style={'color': 'white', "borderWidth": "0.4vh"}),
			dbc.Row([
				dbc.Col([
					html.P(['Year']),
					dcc.Dropdown(options=[2022, 2023], id='bkk_year')
					], width=3),
				dbc.Col([
					html.P(['Receipt Type']),
					dcc.Dropdown(options=[x for x in df23['Receipt Type'].unique()], id='bkk_type')
					], width=3)
				],
				className='mb-3'
				),
			dbc.Row([
				dbc.Col([
					dcc.Graph(figure={}, id='bkk_graph_hsbc', className='mb-3'),
					dcc.Graph(figure={}, id='bkk_graph_bay')
				])
			])
		])
	], class_name='shadow', style={'color': 'rgb(204, 245, 172)', 'background-color': magenta})
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

	dfHsbc22 = change_df(dfBkk22, 'HSBC')
	dfHsbc23 = change_df(dfBkk23, 'HSBC')

	dfBay22 = change_df(dfBkk22, 'BAY')
	dfBay23 = change_df(dfBkk23, 'BAY')

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
		return figHsbc, figBay
	else:
		return figHsbc, figBay

