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

GCdf = pd.read_sql_table("CME_GC", localhost)
CLdf = pd.read_sql_table("CME_CL", localhost)
ESdf = pd.read_sql_table("CME_ES", localhost)
NGdf = pd.read_sql_table("CME_NG", localhost)
NQdf = pd.read_sql_table("CME_NQ", localhost)

app = dash.Dash()

# data_dict = {"Gold": gold_graph,
#              "S&P 100 E-mini": s_and_p_graph,
#              }
# df = pd.read_csv(
#     'CSVs/GC.csv')


def get_contract_family(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {} from futures where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=field)


def create_tables(contract_root):
    df = get_contract_family(contract_root, field='px_last').fillna(method='ffill')
    # pretty_plot(df, title=contract_root, ylabel='px_last')
    df.to_sql(contract_root, localhost, if_exists='replace', chunksize=250)


# create_tables("CME_CL")
# create_tables("CME_ES")
# create_tables("CME_NQ")
# create_tables("CME_NG")
# create_tables("CME_GC")

app.layout = html.Div(children=[
    html.H1('Price Graphs'),
    dcc.Input(id='input', value='Enter Something', type='text'),
    html.Div(id='output'),
    dcc.Dropdown(
        options=[
            {'label': 'Gold', 'value': 'gold_graph'},
            {'label': 'S&P 100 E-mini', 'value': 's_and_p_graph'},
        ],
        placeholder="Select a Contract",
        id="dropdown_data"
    ),
    dcc.Graph(id='gold_graph',
              figure={
                  'data': [
                      {'x': GCdf.datadate, 'y': GCdf.CME_GC1, 'type': 'line', 'name': 'GC1'},
                      {'x': GCdf.datadate, 'y': GCdf.CME_GC2, 'type': 'line', 'name': 'GC2'},
                      {'x': GCdf.datadate, 'y': GCdf.CME_GC3, 'type': 'line', 'name': 'GC3'},
                      {'x': GCdf.datadate, 'y': GCdf.CME_GC4, 'type': 'line', 'name': 'GC4'},

                  ],
                  'layout': {
                      'title': 'Gold Price'
                  }
              }),

    dcc.Graph(id='s_and_p_graph',
              figure={
                  'data': [
                      {'x': ESdf.datadate, 'y': ESdf.CME_ES1, 'type': 'line', 'name': 'ES1'},
                      {'x': ESdf.datadate, 'y': ESdf.CME_ES2, 'type': 'line', 'name': 'ES2'},
                      {'x': ESdf.datadate, 'y': ESdf.CME_ES3, 'type': 'line', 'name': 'ES3'},
                      {'x': ESdf.datadate, 'y': ESdf.CME_ES4, 'type': 'line', 'name': 'ES4'},

                  ],
                  'layout': {
                      'title': 'S&P 100 E-Mini Price'
                  }
              })
])


# @app.callback(
#     Output(component_id='output', component_property='children'),
#     [Input(component_id='input', component_property='value')]
# )
def update_value(dropdown_data):
    return dcc.Graph(dropdown_data)


if __name__ == '__main__':
    app.run_server(debug=True)
