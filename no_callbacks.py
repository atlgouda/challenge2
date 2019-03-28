import dash
# from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlalchemy import create_engine
# import pandas_datareader.data as web
# import datetime

# start = datetime.datetime(2005, 1, 1)
# end = datetime.datetime.now()

localhost = create_engine('mysql://root:password@localhost/solution')

df = pd.read_sql_table("allprices", localhost)

app = dash.Dash()


def get_contract_family(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {} from futures where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=field)


def create_tables(contract_root):
    df = get_contract_family(contract_root, field='px_last').fillna(method='ffill')
    df.to_sql(contract_root, localhost, if_exists='replace', chunksize=250)

# CREATED TABLES WITH THESE FUNCTIONS
# create_tables("CME_CL")
# create_tables("CME_ES")
# create_tables("CME_NQ")
# create_tables("CME_NG")
# create_tables("CME_GC")


app.layout = html.Div(children=[
    html.H1('Price Graphs'),

    dcc.Dropdown(
        id="dropdown_data",
        options=[
            {'label': 'GC1', 'value': 'GC1'},
            {'label': 'GC2', 'value': 'GC2'},
            {'label': 'GC3', 'value': 'GC3'},
            {'label': 'GC4', 'value': 'GC4'},
        ],
        placeholder="Select a Contract",
    ),
    dcc.Graph(id='gold_graph',
              figure={
                  'data': [
                      {'x': df.datadate, 'y': df.CME_GC1, 'type': 'line', 'name': 'GC1'},
                      {'x': df.datadate, 'y': df.CME_GC2, 'type': 'line', 'name': 'GC2'},
                      {'x': df.datadate, 'y': df.CME_GC3, 'type': 'line', 'name': 'GC3'},
                      {'x': df.datadate, 'y': df.CME_GC4, 'type': 'line', 'name': 'GC4'},
                      {'x': df.datadate, 'y': df.CME_ES1, 'type': 'line', 'name': 'ES1'},
                      {'x': df.datadate, 'y': df.CME_ES2, 'type': 'line', 'name': 'ES2'},
                      {'x': df.datadate, 'y': df.CME_ES3, 'type': 'line', 'name': 'ES3'},
                      {'x': df.datadate, 'y': df.CME_ES4, 'type': 'line', 'name': 'ES4'},
                      {'x': df.datadate, 'y': df.CME_CL1, 'type': 'line', 'name': 'CL1'},
                      {'x': df.datadate, 'y': df.CME_CL2, 'type': 'line', 'name': 'CL2'},
                      {'x': df.datadate, 'y': df.CME_CL3, 'type': 'line', 'name': 'CL3'},
                      {'x': df.datadate, 'y': df.CME_CL4, 'type': 'line', 'name': 'CL4'},
                      {'x': df.datadate, 'y': df.CME_NG1, 'type': 'line', 'name': 'NG1'},
                      {'x': df.datadate, 'y': df.CME_NG2, 'type': 'line', 'name': 'NG2'},
                      {'x': df.datadate, 'y': df.CME_NG3, 'type': 'line', 'name': 'NG3'},
                      {'x': df.datadate, 'y': df.CME_NG4, 'type': 'line', 'name': 'NG4'},
                      {'x': df.datadate, 'y': df.CME_NQ1, 'type': 'line', 'name': 'NQ1'},
                      {'x': df.datadate, 'y': df.CME_NQ2, 'type': 'line', 'name': 'NQ2'},
                  ],
                  'layout': {
                      'title': 'Gold Price'
                  }
              }),
])


def update_value(dropdown_data):
    return dcc.Graph(dropdown_data)


if __name__ == '__main__':
    app.run_server(debug=True)
