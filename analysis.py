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


def chart2(df, fields=None, title=None, layout=None, output_type=None, dtick='M1'):
    if not fields:
        fields = df.columns
        # xfields = df2.columns
    if not layout:
        layout = _get_default_layout2(title, dtick)

    traces = []

    for field in fields:
        traces.append(go.Bar(x=df[field], y=df[field], name=field))

    fig = go.Figure(data=traces, layout=layout)
    return plot(fig, output_type=output_type)


def root_table(df, fields=None, title=None, layout=None, output_type=None):
    if not fields:
        fields = df.columns

    traces = []

    for field in fields:
        traces.append(go.Table(
            header=dict(values=list(df.columns),
                        fill=dict(color='#C2D4FF'),
                        align=['left'] * 5),
            cells=dict(values=[df[field]],
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


def _get_default_layout2(title, dtick='dtick'):
    return go.Layout(
        title=title,
        font=dict(family='Saira', size=16, color='#7f7f7f'),
        xaxis={
            'type': 'category',
            'dtick': 'dtick',
            'tickmode': 'array',
            'tickvals': [0, 1, 2, 3],
            'ticktext': [title + '1', title + '2', title + '3', title + '4'],
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


def chart_ann_vol_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='ann_vol').fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


def table_ann_vol_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='ann_vol').fillna(method='ffill')
    return root_table(df, output_type='div', title=contract_root)


def chart_tr_1yr_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='tr_1yr').fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


def chart_daily_return_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='largest_daily_return',
                             ).fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


def chart_annual_return_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field=('largest_annual_return')).fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


def create_csv():
    df = get_contract_family('CME_CL', field='largest_daily_return',).fillna(method='ffill')
    df.to_csv('cl_largest_daily_returns.csv')
    df2 = get_contract_family('CME_CL', field='largest_daily_return_date',).fillna(method='ffill')
    df2.to_csv('cl_largest_daily_returns_date.csv')


create_csv()
