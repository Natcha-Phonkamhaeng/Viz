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

ar_guage = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 0.06, # this value will be change according to AR Dashboard
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
				html.H3(['Overdue Ratio (Overdue VS Total Outstanding'])
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
			]),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(figure=overdue_guage)
					], class_name='shadow')
				], style={'background-color': 'lavender'})
			])
		])
	])