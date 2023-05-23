import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_ag_grid as dag


dash.register_page(__name__, path='/', name='Dishonoured Cheque')

df = pd.read_excel('chq.xlsx')

months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
monthYr = ['Apr22','May22','Jun22','Jul22','Aug22','Sep22','Oct22','Nov22','Dec22','Jan22','Feb22', 'Mar22',
			'Apr23']
vol = [4,1,4,2,1,1,1,1,0,4,1,0,1]

dfTime = pd.DataFrame.from_dict({
	'Month' : monthYr,
	'Volume': vol,
	})

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


fig1 = px.sunburst(bound, path=['Year', 'Month', 'Bound'], values='Volume', color='Volume', title='Bound by month')


layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dcc.Markdown('## Dishonoured Cheque As of Apr 22 - Apr 23', style={'color':'#160c9c', 'textAlign':'center'})
			])
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			my_radio := dcc.RadioItems(options=['Bar Chart', 'Time Series'], value='Bar Chart', inline=True, labelStyle= {"margin":"1rem"})
			])
		]),
	dbc.Row([
		dbc.Col([
			my_graph := dcc.Graph(figure=fig)
			], width=8),
		dbc.Col([
			my_pie := dcc.Graph(figure=fig1)
			], width=4)
		]),
	dbc.Row([
		dbc.Col([
			year_drop:= dcc.Dropdown([x for x in df['Year'].unique()], placeholder='select year')
			], width=2),
		dbc.Col([
			month_drop:= dcc.Dropdown([x for x in df['Month'].unique()], placeholder='select month')
			], width=2)
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			my_table := dag.AgGrid(
				rowData = df.to_dict('records'),
				columnDefs = [
		        {'field': 'Company'},
		        {'field': 'Bound', "headerClass": 'center-header','cellStyle': {'textAlign': 'center'}}, #headerClass is CSS in assets folder
		        {'field': 'Amount', 'type': 'rightAligned', "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'}},
		        {'field': 'Remark'},
		        ],
		        defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
		        columnSize="autoSize",
			    dashGridOptions={"pagination": True, "paginationPageSize":5, "domLayout": "autoHeight"},
			    className="ag-theme-alpine",  # https://dashaggrid.pythonanywhere.com/layout/themes
				)
			])
		])
	])
	
@callback(
	Output(my_graph, 'figure'),
	Output(my_table, 'rowData'),
	Input(my_radio, 'value'),
	Input(year_drop, 'value'),
	Input(month_drop, 'value')
	)
def update(select_radio, select_year, select_month):
	dff = df.copy()
	if select_radio == 'Time Series':
		figLine = px.line(dfTime, x='Month', y='Volume', markers=True, color_discrete_sequence=["#ed0ccf"])
		
		if select_year is not None and select_month is not None:
			mask = (df['Year'] == select_year) & (df['Month'] == select_month)
			dff = dff[mask]
			return figLine, dff.to_dict('records')
		
		return figLine, dff.to_dict('records')
	
	elif select_radio == 'Bar Chart':
		if select_year is not None and select_month is not None:
			mask = (df['Year'] == select_year) & (df['Month'] == select_month)
			dff = dff[mask]
			return fig, dff.to_dict('records')
		return fig, df.to_dict('records')
	


