import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go
from datetime import datetime


dash.register_page(__name__, path='/page-2', name='Container Deposit')
today = datetime.today()

dfIdms = pd.read_excel('idms2.xlsx')
dfIdms['Date'] = dfIdms['date'].dt.strftime('%d-%m-%Y')

months = dfIdms['month'].unique().tolist()

def y_value(col):
	# return value of column with sorted months starting with Jan to Dec
	y_val = dfIdms.sort_values('date').groupby(dfIdms['date'].dt.month_name().str[:3], sort=False)[col].sum().rename_axis('Month').reset_index(name=col)[col].tolist()
	return y_val

fig = go.Figure()

fig.add_trace(go.Bar(x=months, y=y_value('chq received'),
                base=0,
                marker_color='green',
                name='received'
                ))
fig.add_trace(go.Bar(x=months, y=y_value('chq returned'),
                base=[-x for x in y_value('chq returned')],
                hovertemplate=["({} {:,})".format(x,y) for x,y in zip(months, y_value('chq returned'))],
                marker_color='crimson',
                name='returned'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#dae1e6', margin=dict(l=0,r=0,b=0,t=25))



layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H5("Number of Expire Chq", className='text-black'),
					html.H2("1", className='text-black'),
					]),
				color= '#d8f2f0'
				)
			]),
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H5("Customer Chq Expire", className='text-black'),
					html.H2("ABC Company Limited", className='text-black'),
					]),
				color= '#f2d8d8'
				)
			]),
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H5("Details Chq Expire"),
					html.H2("1,234.00 / KBank 1234567"),
					]),
				color= '#f2f1d8'
				)
			])
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			my_graph := dcc.Graph(figure=fig)
			], width=9),
		dbc.Col([
			html.Label('Year', className='bg-primary text-white'),
			continent_drop := dcc.Dropdown([x for x in dfIdms['year'].unique()]),
			html.Label('Month', className='bg-primary text-white'),
			country_drop := dcc.Dropdown([x for x in dfIdms['month'].unique()], multi=True),
			], width=3),
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
				dag.AgGrid(
			    id="my-table",
			    rowData=dfIdms.to_dict("records"),                                                         
			    columnDefs=[
			    {
			    	'field': 'Date',
			    	"headerClass": 'center-header',
			    	'cellStyle': {'textAlign': 'center'},
			    },
			    {
			    	'field': 'chq received',
			    	"valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
			    	'type': 'rightAligned',
			    	"cellStyle": {"color": "green"},
			    },
			    {
			    	'field': 'vol chq received',
			    	'type': 'rightAligned',
			    	"cellStyle": {"color": 'green'},
			    },
			    {
			    	'field': 'chq returned',
			    	"valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
			    	'type': 'rightAligned',
			    	"cellStyle": {"color": "red"},
			    },
			    {
			    	'field': 'vol chq returned',
			    	'type': 'rightAligned',
			    	"cellStyle": {"color": "red"},
			    },
			    ],                                          
			    defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
			    columnSize="sizeToFit",
			    dashGridOptions={"pagination": True, "paginationPageSize":5,"domLayout": "autoHeight"},
			    className="ag-theme-alpine color-fonts",
				),
				html.Label(f'Last update: {today.day}/{today.month}/{today.year}')
			])
		])
	])