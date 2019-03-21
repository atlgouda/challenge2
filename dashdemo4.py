import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'CSV/GC.csv')

app.layout = html.Div([
    dcc.Graph(
        id='gc-graph',
        figure={
            'data': [
                {
                    "type": "scatter",
                    "mode": "lines",
                    "name": "GC1",
                    "x": [df[datadate]],
                    "y": [df[CME_GC1]]
                },
                {
                    "type": "scatter",
                    "mode": "lines",
                    "name": "GC2",
                    "x": [df[df[datadate]]],
                    "y": [df[df[CME_GC2]]]
                }]
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
