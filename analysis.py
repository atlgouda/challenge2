import pandas as pd
import matplotlib  # noqa
from sqlalchemy import create_engine
from plotly.offline import plot
import plotly.graph_objs as go

localhost = create_engine('mysql://root:password@localhost/solution')


def get_contract_family(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {} from futures where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_dated(contract_root, field='largest_daily_return', return_date='largest_daily_return_date'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {}, {} from futures where code_name in {}".format(
        field, return_date, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=[field, return_date])


def chart(df, fields=None, title=None, layout=None, output_type=None, dtick='M1'):
    if not fields:
        fields = df.columns
    if not layout:
        layout = _get_default_layout(title, dtick)

    traces = []

    for field in fields:
        traces.append(go.Scattergl(x=df.index, y=df[field], mode='lines', name=field))

    fig = go.Figure(data=traces, layout=layout)
    return plot(fig, output_type=output_type)


def root_table(df, fields=None, title=None, layout=None, output_type=None):
    if not fields:
        fields = df.columns

    traces = []

    for field in fields:
        traces.append(go.Table(
            header=dict(values=['Code Name', title],
                        fill=dict(color='#C2D4FF'),
                        align=['left'] * 5),
            cells=dict(values=[df.columns, df[fields].max()],
                       fill=dict(color='#F5F8FF'),
                       align=['left'] * 5)
        ))

    fig = go.Figure(data=traces)
    return plot(fig, output_type=output_type)


def root_table_daily(df, fields=None, title=None, layout=None, output_type=None):
    if not fields:
        fields = df.columns

    traces = []

    for field in fields:
        traces.append(go.Table(
            header=dict(values=['Code Name', title, 'Date'],
                        fill=dict(color='#C2D4FF'),
                        align=['left'] * 5),
            cells=dict(values=[df.columns.get_level_values(1).drop_duplicates(),
                               df.dropna().loc[:, 'largest_daily_return'].max(),
                               df.dropna().loc[:, 'largest_daily_return_date'].max()],
                       fill=dict(color='#F5F8FF'),
                       align=['left'] * 5)
        ))

    fig = go.Figure(data=traces)
    return plot(fig, output_type=output_type)


def root_table_annual(df, fields=None, title=None, layout=None, output_type=None):
    if not fields:
        fields = df.columns

    traces = []

    for field in fields:
        traces.append(go.Table(
            header=dict(values=['Code Name', title, 'Date'],
                        fill=dict(color='#C2D4FF'),
                        align=['left'] * 5),
            cells=dict(values=[df.columns.get_level_values(1).drop_duplicates(),
                               df.dropna().loc[:, 'largest_annual_return'].max(),
                               df.dropna().loc[:, 'largest_annual_return_date'].max()],
                       fill=dict(color='#F5F8FF'),
                       align=['left'] * 5)
        ))

    fig = go.Figure(data=traces)
    return plot(fig, output_type=output_type)


def _get_default_layout(title, dtick='M1'):
    return go.Layout(
        title=title,
        font=dict(family='Saira', size=16, color='#7f7f7f'),
        xaxis={
            'type': 'date',
            'dtick': 'M36',
            'tickformat': '%m/%y',
            'hoverformat': '%m/%d/%y',
            'zerolinecolor': 'black',
            'showticklabels': True,
            'zeroline': True,
            'showgrid': True
        },
    )


def chart_contracts_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='px_last').fillna(method='ffill')
    return chart(df, output_type='div', title=contract_root)


def chart_returns_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='daily_return').fillna(method='ffill')
    return chart(df.cumsum(), output_type='div', title=contract_root)


def table_ann_vol_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='ann_vol').fillna(method='ffill')
    return root_table(df, output_type='div', title='Annualized Volatility')


def table_tr_1yr_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='tr_1yr').fillna(method='ffill')
    return root_table(df, output_type='div', title='Trailing 1-year Volatility')


def table_daily_dynamic(contract_root):
    df = get_contract_family_dated('CME_{}'.format(contract_root),
                                   ).fillna(method='ffill')
    return root_table_daily(df, output_type='div', title='Largest Daily Return')


def table_annual_dynamic(contract_root):
    df = get_contract_family_dated('CME_{}'.format(contract_root),
                                   field='largest_annual_return', return_date='largest_annual_return_date').fillna(method='ffill')
    return root_table_annual(df, output_type='div', title='Largest Annual Return')
