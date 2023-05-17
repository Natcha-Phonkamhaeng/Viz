import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

dash.register_page(__name__, path='/', name='Dishonoured Cheque')

df = pd.read_excel('chq.xlsx')
print(df.head(1))

months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']

fig = go.Figure(data=[
	go.Bar(name='FY22', x=months, y=[4,1,4,2,1,1,1,1,0,4,1,0]),
	go.Bar(name='FY23', x=months, y=[1]),
	])
fig.update_layout(barmode='group', title='Volume of dishonoured cheque by year',yaxis={'title': 'No of dishonoured cheque'})

bound = pd.DataFrame.from_dict({
	'Year': ['FY22', 'FY22', 'FY22', 'FY22', 'FY22', 'FY22', 'FY22', 'FY22','FY22', 'FY22', 'FY22', 'FY22', 'FY22','FY23'],
	'Month': ['Apr', 'Apr', 'May', 'Jun','Jul','Jul','Aug','Sep', 'Oct', 'Nov', 'Jan','Jan', 'Feb', 'Apr'],
	'Bound': ['OB', 'IB', 'OB', 'OB', 'OB', 'IB', 'OB', 'IB','OB', 'OB', 'OB', 'IB', 'OB','OB'],
	'Volume': [2,2,1,4,1,1,1,1,1,1,2,2,1,1],
	})


fig1 = px.sunburst(bound, path=['Year', 'Month', 'Bound'], values='Volume', color='Month', title='Bound by month')


layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dcc.Markdown('## Dishonoured Cheque As of Apr 22 - Apr 23', style={'color':'#160c9c', 'textAlign':'center'})
			])
		]),
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='graph-fig', figure=fig)
			], width=8),
		dbc.Col([
			dcc.Graph(id='pie-fig', figure=fig1)
			], width=4)
		]),
	dbc.Row([
		dbc.Col([
			year_drop:= dcc.Dropdown([x for x in df['Year'].unique()], placeholder='select year')
			], width=3),
		dbc.Col([
			month_drop:= dcc.Dropdown([x for x in df['Month'].unique()], placeholder='select month')
			], width=3)
		]),
	dbc.Row([
		dbc.Col([
			my_table := dash_table.DataTable(
		        data=df.to_dict('records'),
		        columns=[
		        {'name': 'Year', 'id': 'Year'},
		        {'name': 'Month', 'id': 'Month'},
		        {'name': 'Company', 'id': 'Company'},
		        {'name': 'Amount', 'id': 'Amount'}
		        ]
		       )
			])
		])
	])
	


