import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd
import time


app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}

app = dash.Dash(__name__)
app.layout = html.Div(
    [html.Div(style={'fontSize': 14, 'font face': 'Century Gothic'}),
       html.H2('SENATORIAL CANDIDATES SENTIMENT ANALYSIS', style={'fontSize': 30, 'font-family': 'Century Gothic', 'font-type': 'bold', 'color': app_colors['someothercolor']
       			, 'text-align': 'center'}),
        # dcc.Input(id='sentiment_term', value='olympic', type='text'),
   #      dcc.Dropdown(id = 'sentiment_term',
   #  	options=[
   #      {'label': 'Bong Go', 'value': 'Bong Go'},
   #      {'label': 'Pilo Hilbay', 'value': 'Pilo Hilbay'},
   #      {'label': 'Duterte', 'value': 'Duterte', 'value': 'duterte'},
   #      {'label': 'a', 'value': 'a'},
   #      ],	
			# ),
   #      dcc.Dropdown(id = 'sentiment_term2',
   #  	options=[
   #      {'label': 'Bong Go', 'value': 'Bong Go'},
   #      {'label': 'Pilo Hilbay', 'value': 'Pilo Hilbay'},
   #      {'label': 'Duterte', 'value': 'Duterte', 'value': 'duterte'},
   #      {'label': 'apple', 'value': 'apple'},
   #      ],	
			# ),
        html.Div([
        html.Div([
        dcc.Dropdown(id = 'sentiment_term',
    	options=[
        {'label': 'Bong Go', 'value': 'Bong Go', 'value': 'bong go'},
        {'label': 'Pilo Hilbay', 'value': 'Pilo Hilbay','value': 'Hilbay', 'value': 'hilbay' },
        {'label': 'Duterte', 'value': 'Duterte', 'value': 'duterte'},
        {'label': 'a', 'value': 'a'},
        {'label': 'the', 'value': 'the'},
        ],style = {'font': app_colors['background']}),
            html.H3('Senator 1', style={'fontSize': 30, 'font-family': 'Century Gothic', 'font-type': 'bold'
       			, 'text-align': 'center','color': app_colors['someothercolor']}),
            dcc.Graph(id = 'live-graph', animate=False)
        ], className="six columns"),

        html.Div([
        dcc.Dropdown(id = 'sentiment_term2',
    	options=[
        {'label': 'Bong Go', 'value': 'Bong Go'},
        {'label': 'Pilo Hilbay', 'value': 'Pilo Hilbay'},
        {'label': 'Duterte', 'value': 'Duterte', 'value': 'duterte'},
        {'label': 'apple', 'value': 'apple'},
        ],
			),
            html.H3('Senator 2', style={'fontSize': 30, 'font-family': 'Century Gothic', 'font-type': 'bold'
       			, 'text-align': 'center','color': app_colors['someothercolor']}),
            dcc.Graph(id = 'live-graph2', animate=False)
        ], className="six columns"),

    ], className="row"),

        	dcc.Interval(
            id='graph-update',
            interval=1*1000
        	),


    ],style={'backgroundColor': app_colors['background'], 'margin-top':'-10px', 'height':'1000px',},

)
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(sentiment_term):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 200", conn ,params=('%' + sentiment_term + '%',))
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/2)).mean()

        df['date'] = pd.to_datetime(df['unix'],unit='ms')
        df.set_index('date', inplace=True)
        df.dropna(inplace=True)
        X = df.index
        Y = df.sentiment_smoothed

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Sentiment',
                mode= 'lines',
                yaxis='y2',
                line = dict(color = (app_colors['sentiment-plot']),
                            width = 4,)
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                     font={'color':app_colors['text']},
                                                     plot_bgcolor = app_colors['background'],
                                                     paper_bgcolor = app_colors['background'],
                                                    title='Term: {}'.format(sentiment_term))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

@app.callback(Output('live-graph2', 'figure'),
              [Input(component_id='sentiment_term2', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(sentiment_term2):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 200", conn ,params=('%' + sentiment_term2 + '%',))
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/2)).mean()

        df['date'] = pd.to_datetime(df['unix'],unit='ms')
        df.set_index('date', inplace=True)
        df.dropna(inplace=True)
        X = df.index
        Y = df.sentiment_smoothed
        
        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Sentiment',
                mode= 'lines',
                yaxis='y2',
                line = dict(color = (app_colors['sentiment-plot']),
                            width = 4,)
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    font={'color':app_colors['text']},
                                                    plot_bgcolor = app_colors['background'],
                                                    paper_bgcolor = app_colors['background'],
                                                    title='Term: {}'.format(sentiment_term2))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)