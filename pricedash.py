import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlalchemy import create_engine
import pdb

localhost = create_engine('mysql://root:password@localhost/solution')

app = dash.Dash()

df = pd.read_sql_table("allprices", localhost)
df2 = pd.read_sql_table("allcumsumreturns", localhost)

all_options = {
    'Gold': ["GC1", "GC2", "GC3", "GC4"],
    'Natural Gas': ["NG1", "NG2", "NG3", "NG4"],
    'Crude Oil': ["CL1", "CL2", "CL3", "CL4"],
    'S&P E-mini': ["ES1", "ES2", "ES3", "ES4"],
    'Nasdaq 100 E-mini': ["NQ1", "NQ2"],
    'All': ["GC1", "GC2", "GC3", "GC4", "NG1", "NG2", "NG3", "NG4",
            "CL1", "CL2", "CL3", "CL4", "ES1", "ES2", "ES3", "ES4", "NQ1", "NQ2"]
}

app.layout = html.Div(id='dashgraphs', children=[
    html.H1(children="Contract Prices"),
    html.Div(
        [
            html.P('Choose Root:'),
            dcc.RadioItems(
                id='root',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='Gold',
                labelStyle={'display': 'inline-block'}
            ),
        ]),
    dcc.Checklist(
        id='contract_number',
        values=['GC1'],
        labelStyle={'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(
            id='example-graph',
        )
    ]),
    html.Div([
        dcc.Graph(
            id='returns-graph',
        )
    ])
])


@app.callback(
    dash.dependencies.Output('contract_number', 'options'),
    [dash.dependencies.Input('root', 'value')])
def set_contract_number_options(selected_root):
    return [{'label': i, 'value': i} for i in all_options[selected_root]]


@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('contract_number', 'values')])
def update_image_src(selector):
    data = []
    if 'GC1' in selector:
        data.append({'x': df.datadate, 'y': df.CME_GC1, 'type': 'line', 'name': 'CME_GC1'})
    if 'GC2' in selector:
        data.append({'x': df.datadate, 'y': df.CME_GC2, 'type': 'line', 'name': 'CME_GC2'})
    if 'GC3' in selector:
        data.append({'x': df.datadate, 'y': df.CME_GC3, 'type': 'line', 'name': 'CME_GC3'})
    if 'GC4' in selector:
        data.append({'x': df.datadate, 'y': df.CME_GC4, 'type': 'line', 'name': 'CME_GC4'})
    if 'NG1' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NG1, 'type': 'line', 'name': 'CME_NG1'})
    if 'NG2' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NG2, 'type': 'line', 'name': 'CME_NG2'})
    if 'NG3' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NG3, 'type': 'line', 'name': 'CME_NG3'})
    if 'NG4' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NG4, 'type': 'line', 'name': 'CME_NG4'})
    if 'CL1' in selector:
        data.append({'x': df.datadate, 'y': df.CME_CL1, 'type': 'line', 'name': 'CME_CL1'})
    if 'CL2' in selector:
        data.append({'x': df.datadate, 'y': df.CME_CL2, 'type': 'line', 'name': 'CME_CL2'})
    if 'CL3' in selector:
        data.append({'x': df.datadate, 'y': df.CME_CL3, 'type': 'line', 'name': 'CME_CL3'})
    if 'CL4' in selector:
        data.append({'x': df.datadate, 'y': df.CME_CL4, 'type': 'line', 'name': 'CME_CL4'})
    if 'ES1' in selector:
        data.append({'x': df.datadate, 'y': df.CME_ES1, 'type': 'line', 'name': 'CME_ES1'})
    if 'ES2' in selector:
        data.append({'x': df.datadate, 'y': df.CME_ES2, 'type': 'line', 'name': 'CME_ES2'})
    if 'ES3' in selector:
        data.append({'x': df.datadate, 'y': df.CME_ES3, 'type': 'line', 'name': 'CME_ES3'})
    if 'ES4' in selector:
        data.append({'x': df.datadate, 'y': df.CME_ES4, 'type': 'line', 'name': 'CME_ES4'})
    if 'NQ1' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NQ1, 'type': 'line', 'name': 'CME_NQ1'})
    if 'NQ2' in selector:
        data.append({'x': df.datadate, 'y': df.CME_NQ2, 'type': 'line', 'name': 'CME_NQ2'})

    figure = {
        'data': data,
        'layout': {
            'title': 'Price Graph',
            'xaxis': dict(
                title='Date',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#7f7f7f'
                )),
            'yaxis': dict(
                title='Price',
                titlefont=dict(
                    family='Helvetica, monospace',
                    size=20,
                    color='#7f7f7f'
                ))
        }
    }
    return figure


@app.callback(
    dash.dependencies.Output('returns-graph', 'figure'),
    [dash.dependencies.Input('contract_number', 'values')])
def update_image_src(selector):
    data = []
    if 'GC1' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_GC1, 'type': 'line', 'name': 'CME_GC1'})
    if 'GC2' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_GC2, 'type': 'line', 'name': 'CME_GC2'})
    if 'GC3' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_GC3, 'type': 'line', 'name': 'CME_GC3'})
    if 'GC4' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_GC4, 'type': 'line', 'name': 'CME_GC4'})
    if 'NG1' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NG1, 'type': 'line', 'name': 'CME_NG1'})
    if 'NG2' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NG2, 'type': 'line', 'name': 'CME_NG2'})
    if 'NG3' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NG3, 'type': 'line', 'name': 'CME_NG3'})
    if 'NG4' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NG4, 'type': 'line', 'name': 'CME_NG4'})
    if 'CL1' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_CL1, 'type': 'line', 'name': 'CME_CL1'})
    if 'CL2' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_CL2, 'type': 'line', 'name': 'CME_CL2'})
    if 'CL3' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_CL3, 'type': 'line', 'name': 'CME_CL3'})
    if 'CL4' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_CL4, 'type': 'line', 'name': 'CME_CL4'})
    if 'ES1' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_ES1, 'type': 'line', 'name': 'CME_ES1'})
    if 'ES2' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_ES2, 'type': 'line', 'name': 'CME_ES2'})
    if 'ES3' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_ES3, 'type': 'line', 'name': 'CME_ES3'})
    if 'ES4' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_ES4, 'type': 'line', 'name': 'CME_ES4'})
    if 'NQ1' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NQ1, 'type': 'line', 'name': 'CME_NQ1'})
    if 'NQ2' in selector:
        data.append({'x': df2.datadate, 'y': df2.CME_NQ2, 'type': 'line', 'name': 'CME_NQ2'})

    figure = {
        'data': data,
        'layout': {
            'title': 'Returns Graph',
            'xaxis': dict(
                title='Date',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#7f7f7f'
                )),
            'yaxis': dict(
                title='Cumulative Sum Returns',
                titlefont=dict(
                    family='Helvetica, monospace',
                    size=20,
                    color='#7f7f7f'
                ))
        }
    }
    return figure


def show_graphs():
    return (app.layout)


if __name__ == '__main__':
    app.run_server(debug=True)
