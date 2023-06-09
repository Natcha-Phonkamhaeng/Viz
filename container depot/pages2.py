import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go

dash.register_page(__name__, path='/page-2', name='Container Deposit')

magenta = '#db0f72'
dfIdms = pd.read_excel('data/idms2.xlsx')
dfIdms['Date'] = dfIdms['date'].dt.strftime('%d-%m-%Y')

months = dfIdms['month'].unique().tolist()

def y_value(col):
	# return value of column with sorted months starting with Jan to Dec
	y_val = dfIdms.sort_values('date').groupby(dfIdms['date'].dt.month_name().str[:3], sort=False)[col].sum().rename_axis('Month').reset_index(name=col)[col].tolist()
	return y_val

fig = go.Figure(
    data=[
        go.Bar(name='received', x=months, y=y_value('chq received'), marker_color='green', text=y_value("chq received")),
        go.Bar(name='returned', x=months, y=y_value('chq returned'), marker_color='red', text=y_value('chq returned'))
    ]
)

fig.update_layout(template='simple_white')
fig.update_traces(texttemplate='%{text:,}')

col = [
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
	]


layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H4(children=[html.I(className="bi bi-cash-coin me-2"), "Number of Expire Chq"],className="text-nowrap"),
					html.H4("0"),
					],className="border-start border-danger border-5"
					),
				className='text-center m-4 bg-primary text-white',
				)
			]),
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H4(children=[html.I(className="bi bi-currency-exchange me-2"), "Customer Chq Expire"],className="text-nowrap"),
					html.H4("-", className="text-nowrap"),
					],className="border-start border-danger border-5"
					),
				className='text-center m-4 bg-primary text-white',
				)
			]),
		dbc.Col([
			dbc.Card(
				dbc.CardBody([
					html.H4(children=[html.I(className="bi bi-bank me-2"), "Detail Chq Expire"], className="text-nowrap"),
					html.H4("-", className="text-nowrap"),
					],className="border-start border-danger border-5"
					),
				className='text-center m-4 bg-primary text-white',
				)
			])
		]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			my_graph := dcc.Graph(figure=fig)
			], width=9),
		dbc.Col([
			my_radio := dcc.RadioItems(options=['Cheque', 'Insurance'], value='Cheque', inline=True, labelStyle= {"margin":"1rem"}),
			html.Label('Year', className='bg-primary text-white'),
			year_drop := dcc.Dropdown([x for x in dfIdms['year'].unique()]),
			html.Label('Month', className='bg-primary text-white'),
			month_drop := dcc.Dropdown([x for x in dfIdms['month'].unique()], multi=True),
			html.Label('Viewed By', className='bg-primary text-white'),
			view_drop := dcc.Dropdown(['Total Amt', 'Transaction'], placeholder='Total Amt')
			], width=3),
		]),
	dbc.Row([
		dbc.Col([
			my_btn := dbc.Button(children=[html.I(className='bi bi-cloud-arrow-down me-2'), 'Download Excel']),
			download := dcc.Download()
			])
		], className='mb-2'),
	dbc.Row([
		dbc.Col([
				my_table := dag.AgGrid(
			    rowData=dfIdms.to_dict("records"),                                                         
			    columnDefs=col,                                          
			    defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
			    columnSize="sizeToFit",
			    dashGridOptions={"pagination": True, "paginationPageSize":5,"domLayout": "autoHeight"},
			    className="ag-theme-alpine color-fonts",
				)
			])
		])
	])

@callback(
	Output(my_graph, 'figure'),
	Output(my_table, 'rowData'),
	Output(my_table, 'columnDefs'),
	Input(my_radio, 'value'), 
	Input(year_drop, 'value'),
	Input(month_drop, 'value'),
	Input(view_drop, 'value'),
	)
def update(select_radio, select_year, select_month, select_view):
	dff = dfIdms.copy()

	if select_radio == 'Cheque':
		if select_year and select_month:
			mask = (dff['year'] == select_year) & (dff['month'].isin(select_month))
			dff = dff[mask]
			if select_view == 'Transaction':
				fig1 = go.Figure(
			    data=[
			        go.Bar(name='received', x=months, y=y_value('vol chq received'), marker_color='green', text=y_value('vol chq received')),
			        go.Bar(name='returned', x=months, y=y_value('vol chq returned'),marker_color='red', text=y_value('vol chq returned'))
			    	]
				)
				fig1.update_layout(template='simple_white', barmode='stack')
				return fig1, dff.to_dict('records'), col
			return fig, dff.to_dict('records'), col
		else:
			return fig, dfIdms.to_dict('records'), col
	
	elif select_radio == 'Insurance':
		fig2 = px.area(dff, x=months, y=y_value('insurance received'))
		fig2.update_layout(yaxis={'title': 'Received Amount'}, xaxis={'title': ''})
		
		colIns =[
	    {
	    	'field': 'Date',
	    	"headerClass": 'center-header',
	    	'cellStyle': {'textAlign': 'center'},
	    },
	    {
	    	'field': 'insurance received',
	    	'type': 'rightAligned',
	    	"valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
	    },
	    {
	    	'field': 'vol insurance received',
	    	'type': 'rightAligned',
	    }
	 ]

		if select_year and select_month:
			mask = (dff['year'] == select_year) & (dff['month'].isin(select_month))
			dff = dff[mask]
			if select_view == 'Transaction':
				fig1 = go.Figure(data=[go.Bar(x=months, y=y_value('vol insurance received'), text=y_value('vol insurance received'))])
				fig1.update_layout(template='simple_white')
				return fig1, dff.to_dict('records'), colIns
			return fig2, dff.to_dict('records'), colIns
		return fig2, dfIdms.to_dict('records'), colIns


@callback(
	Output(download, 'data'),
	Input(my_btn, 'n_clicks'),
	prevent_initial_call = True,
	)
def download(n_clicks):
	dff = dfIdms.copy()
	dff['date'] = dff['date'].dt.strftime('%d-%m-%Y')
	dff = dff.drop(columns=['Date'])
	output = dcc.send_data_frame(dff.to_excel, "container deposit.xlsx", sheet_name="Sheet_1", index=False)
	return output








