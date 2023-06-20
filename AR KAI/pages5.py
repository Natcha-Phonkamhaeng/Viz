import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/page-5', name='AR KAR KPI', order=5)

magenta = '#db0f72'

df_ar_kpi = pd.DataFrame.from_dict({
    'Measurement': ['1 - Unsatisfactory', '2 - Needs Improvement', '3 - Meets Expectations', '4 - Exceeds Expectations', '5 - Excellent'],
    'Criteria': ['>1.7%', '1.01% - 1.70%', '0.50% - 1.00%', '0.01% - 0.49%', '0%']
})

df_overdue_kpi = pd.DataFrame.from_dict({
    'Measurement': ['1 - Unsatisfactory', '2 - Needs Improvement', '3 - Meets Expectations', '4 - Exceeds Expectations', '5 - Excellent'],
    'Criteria': ['>23%', '16.01 - 23.00%', '15.01% - 16.00%', '14.01% - 15.00%', '0% - 14.00%']                 
})

df60Days = pd.DataFrame.from_dict({
    'Month': ['Apr', 'May'],
    'Result': [0.0004, 0.0006],
})

dfOverDue = pd.DataFrame.from_dict({
    'Month': ['Apr', 'May'],
    'Result': [0.18, 0.25],
})


ar_guage = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 0.06, # this value will be change according to AR Dashboard
    number= {'suffix': '%'},
    mode = "gauge+number",
    title = {'text': "AR >60 days KPI : Exceeds Expectations", 'font': {'color':'green', 'size': 28}},
    gauge = {'axis': {'range': [None, 2]},
			'bar': {'color': magenta},
            'steps' : [
                 {'range': [0, 0.49], 'color': "olivedrab"},
                 {'range': [0.49, 1], 'color': "palegreen"},
                 {'range': [1, 1.70], 'color': "yellow"},
                 {'range': [1.70, 2], 'color': "red"},
                 ],
             'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': 1.7}}))
ar_guage.update_layout(margin=dict(l=0, r=0, t=0, b=0),font={'color':'green'},paper_bgcolor = "lavender")

overdue_guage = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 25, # this value will be change according to AR Dashboard
    number= {'suffix': '%'},
    mode = "gauge+number",
    title = {'text': "Overdue Ratio KPI : Unsatisfactory", 'font': {'color':'red', 'size': 30}},
    gauge = {'axis': {'range': [None, 25]},
             'bar': {'color': magenta},
             'steps' : [
                 {'range': [0, 14], 'color': "olivedrab"},
                 {'range': [14, 15], 'color': "palegreen"},
                 {'range': [15, 16], 'color': "yellow"},
                 {'range': [16, 23], 'color': "brown"},
                 {'range': [23, 25], 'color': "red"},
                 ],
             'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': 23}}))
overdue_guage.update_layout(margin=dict(l=0, r=0, t=0, b=0), font={'color':'red'},paper_bgcolor = "lavender")

fig60Days = go.Figure(data=go.Scatter(x=df60Days['Month'].tolist(), y=df60Days['Result'].tolist()))
fig60Days.update_layout(yaxis={'tickformat':".2%"}, 
		yaxis_range=[0,0.0010], 
		title='AR > 60 days VS total outstanding',
		title_font_color='blue',
		title_font_size=30,
		paper_bgcolor='lavender',
		plot_bgcolor="rgba(0,0,0,0)")

figOverDue = go.Figure(data=go.Scatter(x=dfOverDue['Month'].tolist(), y=dfOverDue['Result'].tolist()))
figOverDue.update_layout(yaxis={'tickformat':".2%"}, 
		yaxis_range=[0,0.30], 
		title='Overdue Ratio (Overdue VS Total Outstanding)',
		title_font_color='blue',
		title_font_size=30,
		paper_bgcolor='lavender',
		plot_bgcolor="rgba(0,0,0,0)")

layout = dbc.Container([
	html.Label(['Remark: Aging as at 01 May 2023'], className='mb-4'),
	dbc.Row([
		dbc.Col([
			dbc.CardHeader([
				html.H3(['AR > 60 days VS total outstanding'])
				]),	
			dag.AgGrid(
				rowData= df_ar_kpi.to_dict('records'),
				columnDefs=[{'field': i} for i in df_ar_kpi.columns],
				defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
				columnSize="autoSize",
	    		dashGridOptions={"pagination": True, "paginationPageSize":5, "domLayout": "autoHeight"},
	    		className="ag-theme-alpine color-fonts",
				)
			]),
		dbc.Col([
			dbc.CardHeader([
				html.H3(['Overdue Ratio (Overdue VS Total Outstanding)'])
				]),	
			dag.AgGrid(
				rowData= df_overdue_kpi.to_dict('records'),
				columnDefs=[{'field': i} for i in df_overdue_kpi.columns],
				defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
				columnSize="autoSize",
	    		dashGridOptions={"pagination": True, "paginationPageSize":5, "domLayout": "autoHeight"},
	    		className="ag-theme-alpine color-fonts",
				)
			])
		]),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(figure=ar_guage)
					], class_name='shadow')
				], style={'background-color': 'lavender'})
			], width=6),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(figure=overdue_guage)
					], class_name='shadow')
				], style={'background-color': 'lavender'})
			], width=6)
		], class_name='mb-5'),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(figure=fig60Days),
					], class_name='shadow')
				], style={'background-color': 'lavender'})
			])
		], class_name='mb-5'),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(figure=figOverDue)
					], class_name='shadow')
				], style={'background-color': 'lavender'})
			])
		])
	])