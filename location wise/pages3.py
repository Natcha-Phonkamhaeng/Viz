import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/page-3', name='Location Wise', order=3)

magenta = '#db0f72'

def change_df(dataframe, location, bank):
  mask = (dataframe['Office'] == location) & (dataframe['Bank Account'] == bank)
  return dataframe[mask]

df22 = pd.read_csv('data/Location Wise 22.csv')
df23 = pd.read_csv('data/Location Wise 23.csv')
dfChqVol = pd.read_excel('data/chq volume.xlsx')

BkkVol = px.histogram(dfChqVol[dfChqVol['location'] == 'BKKBB'], x='month', y='volume', color='year', barmode='group')
BkkVol.update_layout(title={'text': 'BKK Chq Volume', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)',
						plot_bgcolor="rgba(0,0,0,0)")

LcbVol = px.histogram(dfChqVol[dfChqVol['location'] == 'LCBBB'], x='month', y='volume', color='year', barmode='group')
LcbVol.update_layout(title={'text': 'LCB Chq Volume', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)',
						plot_bgcolor="rgba(0,0,0,0)")

layout = dbc.Container([
	dbc.Card([
		dbc.CardHeader([
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
					dcc.Markdown(children='', id='my_location', style={'font-size': 35, 'color':'white'})
					])
				])
			],
			style={'color':'white', 'background-color':magenta}
			),
		dbc.CardBody([
			dbc.Row([
				dbc.Col([
					html.P(['Comparison']),
					dcc.Dropdown(options=['By Receipt Type', 'By Month', 'By Accumulative'], placeholder='By Receipt Type',id='my_dropdown'),
					html.Hr(),
					html.P(['Summary:']),
					dcc.Markdown(children='', id='my_note',dangerously_allow_html=True),
					], width=3),
				dbc.Col([
					dcc.Graph(figure={}, id='top_graph', className='mb-3'),
					dcc.Graph(figure={}, id='bottom_graph')
					], width=9)	
				])	
			])
		], class_name='shadow', style={'color': 'black'}),
	html.Br(),
	html.Br(),
	html.Br(),
	dbc.Card([
		dbc.CardHeader([
				html.H2(['CHQ Volume'], style={'color':'white', 'text-align':'center'})
				], style={'background-color': magenta}),
		dbc.CardBody([
			dbc.Row([
				dbc.Col([
					dcc.Graph(figure=BkkVol, className='mb-3'),
					dcc.Graph(figure=LcbVol)
					])
				])
			], class_name='shadow', style={'color': 'black'})
		])
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
			return figHsbc, figBay, ['''\n<p><span style="color: blue">HSBC</span></p>''']+\
			['''\n**Between FY22-FY23**''']+\
			['''\n<p><span style="color: red">Apr -53.43%</span>.</p>''']+\
			['''\n<p><span style="color: red">May -55.10%</span>.</p>''']+\
			['''\n**In Year 2023**''']+\
			['''\n<p><span style="color: red">Apr-May -0.30%</span>.</p>''']+\
			['''\n<p><span style="color: blue">BAY</span></p>''']+\
			['''\n**Between FY22-FY23**''']+\
			['''\n<p><span style="color: red">Apr -44.97%</span>.</p>''']+\
			['''\n<p><span style="color: red">May -38.18%</span>.</p>''']+\
			['''\n**In Year 2023**''']+\
			['''\n<p><span style="color: green">Apr-May 17.75%</span>.</p>''']

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
			return figHsbc, figBay, note+\
			['''\n**HSBC**''']+\
			['''\n<p><span style="color: red">BTR -58.15%</span>.</p>''']+\
			['''\n<p><span style="color: red">CHQ -65.05%</span>.</p>''']+\
			['''\n<p><span style="color: green">E-PAYMENT 21.51%</span>.</p>''']+\
			['''\n**BAY**''']+\
			['''\n<p><span style="color: red">BTR -68.03%</span>.</p>''']+\
			['''\n<p><span style="color: red">CHQ -36.55%</span>.</p>''']+\
			['''\n<p><span style="color: red">CASH -35.94%</span>.</p>''']

	# 2) LCB Location
	elif select_location == ['LAEM CHABANG']:
		dfLcb = change_df(df,'LCBBB', 'BAY')
		dfLcb.insert(6,'Bank', np.nan)
		mask = (dfLcb['Receipt Type'] == 'CHQ') | (dfLcb['Receipt Type'] == 'CSH')
		dfLcb.loc[mask, ['Bank']] = 'BILL'
		dfLcb.loc[~mask, ['Bank']] = 'SAVING'
		dfLcbGroup = dfLcb.groupby(['Receipt Type', 'Bank Account', 'Year'])[['Total Amount']].agg('sum').reset_index()
		
		fig = px.histogram(dfLcbGroup, x='Receipt Type', y='Total Amount', color='Year', barmode='group')
		fig.update_layout(title={'text': 'LCB', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")
		
		fig1 = px.icicle(dfLcb, path=[px.Constant('BAY'), 'Bank', 'Year', 'Receipt Type'], values='Total Amount')
		fig1.update_layout(title={'text': 'LCB', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)",
					margin=dict(t=0, l=0, r=0, b=0))

		if select_type == 'By Month':
			dfLcbGroup = dfLcb.groupby(['Year', 'Month'])[['Total Amount']].agg('sum').reset_index()
			fig = px.histogram(dfLcbGroup, x='Month', y='Total Amount', color='Year', barmode='group')
			fig.update_layout(title={'text': 'LCB', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

			fig1 = px.icicle(dfLcb, path=[px.Constant('BAY'), 'Bank', 'Year', 'Month'], values='Total Amount')
			fig1.update_layout(title={'text': 'LCB', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)",
					margin=dict(t=0, l=0, r=0, b=0))
			return fig, fig1, ['''\n**Between FY22-FY23**''']+\
			['''\n<p><span style="color: red">Apr -68.17%</span>.</p>''']+\
			['''\n<p><span style="color: red">May -69.04%</span>.</p>''']+\
			['''\n**In Year 2023**''']+\
			['''\n<p><span style="color: green">Apr-May 17.71%</span>.</p>''']

		elif select_type == 'By Accumulative':
			dfLcbGroup = dfLcb.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
			dfLcbGroup['Accu'] = dfLcbGroup.groupby('Year').cumsum(numeric_only=True)
			
			fig = go.Figure()
			fig.add_trace(go.Scatter(x=dfLcbGroup['Month'].unique().tolist(), y=dfLcbGroup[dfLcbGroup['Year'] == 2022]['Accu'].tolist(), name='FY22',fill='tozeroy'))
			fig.add_trace(go.Scatter(x=dfLcbGroup['Month'].unique().tolist(), y=dfLcbGroup[dfLcbGroup['Year'] == 2023]['Accu'].tolist(), name='FY23',fill='tozeroy'))
			fig.update_layout(title={'text': 'Bay', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)', 
						plot_bgcolor="rgba(0,0,0,0)")

			fig1 = px.histogram(dfLcb, x='Bank', y='Total Amount', color='Year', barmode='group')
			fig1.update_layout(title={'text': 'LCB', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")
			return fig, fig1, note
		else: # default By Receipt Type
			return fig, fig1, note+\
			['''\n**LCB**''']+\
			['''\n<p><span style="color: red">BTR -68.53%</span>.</p>''']+\
			['''\n<p><span style="color: red">CHQ -69.31%</span>.</p>''']+\
			['''\n<p><span style="color: red">CASH -81.28%</span>.</p>''']

	# 3) Songkhla Location
	elif select_location == ['SONGKHLA']:
		dfSgz = change_df(df,'SGZBB', 'BAY')
		if select_type == 'By Month':
			dfSgzGroup = dfSgz.groupby(['Year', 'Month'])[['Total Amount']].agg('sum').reset_index()
			fig = px.histogram(dfSgzGroup, x='Month', y='Total Amount', color='Year', barmode='group')
			fig.update_layout(title={'text': 'SGZ', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

			fig1 = px.icicle(dfSgz, path=[px.Constant('BAY'), 'Year', 'Month'], values='Total Amount')
			fig1.update_layout(title={'text': 'SGZ', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)",
					margin=dict(t=0, l=0, r=0, b=0))
			return fig, fig1, ['''\n**Between FY22-FY23**''']+\
			['''\n<p><span style="color: red">Apr -56.15%</span>.</p>''']+\
			['''\n<p><span style="color: red">May -28.66%</span>.</p>''']+\
			['''\n**In Year 2023**''']+\
			['''\n<p><span style="color: green">Apr-May 51.34%</span>.</p>''']
		elif select_type == 'By Accumulative':
			dfSgzGroup = dfSgz.groupby(['Month', 'Year'])[['Total Amount']].agg('sum').reset_index()
			dfSgzGroup['Accu'] = dfSgzGroup.groupby('Year').cumsum(numeric_only=True)
			
			fig = go.Figure()
			fig.add_trace(go.Scatter(x=dfSgzGroup['Month'].unique().tolist(), y=dfSgzGroup[dfSgzGroup['Year'] == 2022]['Accu'].tolist(), name='FY22',fill='tozeroy'))
			fig.add_trace(go.Scatter(x=dfSgzGroup['Month'].unique().tolist(), y=dfSgzGroup[dfSgzGroup['Year'] == 2023]['Accu'].tolist(), name='FY23',fill='tozeroy'))
			fig.update_layout(title={'text': 'Bay', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
						paper_bgcolor='rgb(176,196,222)', 
						plot_bgcolor="rgba(0,0,0,0)")

			fig1 = px.icicle(dfSgz, path=[px.Constant('BAY'), 'Year', 'Month'], values='Total Amount')
			fig1.update_layout(title={'text': 'SGZ', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)",
					margin=dict(t=0, l=0, r=0, b=0))
			return fig, fig1, note
		else: # By Receipt Type
			dfSgzGroup = dfSgz.groupby(['Receipt Type', 'Bank Account', 'Year'])[['Total Amount']].agg('sum').reset_index()
			fig = px.histogram(dfSgzGroup, x='Receipt Type', y='Total Amount', color='Year', barmode='group')
			fig.update_layout(title={'text': 'SGZ', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)")

			fig1 = px.icicle(dfSgz, path=[px.Constant('BAY'), 'Year', 'Month'], values='Total Amount')
			fig1.update_layout(title={'text': 'SGZ', 'x': 0.5, 'font':{'color':'blue', 'size': 25}}, 
					paper_bgcolor='rgb(176,196,222)', 
					plot_bgcolor="rgba(0,0,0,0)",
					margin=dict(t=0, l=0, r=0, b=0))
			return fig, fig1, note+\
			['''\n**SGZ**''']+\
			['''\n<p><span style="color: red">BTR -42.91%</span>.</p>''']

	else:
			return figHsbc, figBay, note
	
	
