import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Home Page'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3, 4],
                 'y': [0.19455581814423878,
                       0.19608752418685949,
                       0.18966625453774866,
                       0.06506962753429779],
                 'type': 'line', 'name': 'ES Annualized Vol'},
                {'x': [1, 2, 3, 4],
                 'y': [0.3782472231416219,
                       0.3367660992693855,
                       0.3160926808453774,
                       0.3022044197655697],
                 'type': 'line', 'name': 'CL Annualized Vol'},
                {'x': [1, 2, 3, 4],
                 'y': [0.5650552682752835,
                       0.49955685847580583,
                       0.4469644657443433,
                       0.39386359508063445],
                 'type': 'line', 'name': 'NG Annualized Vol'},
                {'x': [1, 2, 3, 4],
                 'y': [0.20657791754251123,
                       0.19361273976588836,
                       0.19482655293143833,
                       0.20010911553140906],
                 'type': 'line', 'name': 'GC Annualized Vol'},
                {'x': [1, 2],
                 'y': [0.27690176423176344,
                       0.2738555077926111],
                 'type': 'line', 'name': 'NQ Annualized Vol'},
                # {'x': [1, 2, 3, 4], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
