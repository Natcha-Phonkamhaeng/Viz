import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/page-1', name='Dishonoured Cheque')

chqCounts = pd.DataFrame(dict(
    month = ['Apr22', 'May22', 'Jun22', 'Jul22', 'Aug22','Sep22', 
    		'Oct22', 'Nov22', 'Dec22','Jan23', 'Feb23', 'Mar23', 'Apr23'],
    counts = [4,1,4,2,1,1,1,1,0,4,1,0,1]
))

df_ = pd.read_excel('chq.xlsx')
df = df_.copy()
fig = px.line(chqCounts, x="month", y="counts",markers=True)
fig.update_layout(xaxis_title='', yaxis_title='number of dishonoured cheque')

CARD_STYLE = {
	"background-color": "#e1eef0"
}


layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			dcc.Markdown('## Dishonoured Cheque As of Apr 22 - Apr 23', style={'color':'#160c9c', 'textAlign':'center'})
			]),
		html.Br(),
		]),
	dbc.Row([
		dbc.Col([
			dcc.Dropdown(['Overview', 'Monthly Detail'], placeholder='Overview')
			])
		]),
	dbc.Row([
		dbc.Col([
				dcc.Graph(id='graph-fig', figure=fig)
			])
		]),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4('Total'),
					html.H1(f'{df.shape[0]}'),
					html.H6('of dishonoured cheque')
					])
				],style=CARD_STYLE)
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4('Most Reason'),
					html.H1(f'{df.value_counts("Reason").reset_index()["Reason"][0]}'),
					html.H6('Drawer\'s signature')
					])
				],style=CARD_STYLE)
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4('Most is Outbound'),
					html.H1(15),
					html.H6('While Inbound is 6')
					])
				],style=CARD_STYLE)
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4('Max Amount'),
					html.H1('910,610.47'),
					html.H6('By Thai Fresh Products')
					])
				],style=CARD_STYLE)
			])
		])
	])
		


