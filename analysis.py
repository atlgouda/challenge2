import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib  # noqa
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
import math
from plotly.offline import plot
import plotly.graph_objs as go

localhost = create_engine('mysql://root:password@localhost/solution')


def get_contract_family(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {} from futures where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_daily(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select date, code_name, {} from combined_largest_daily_return where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='date')
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_annual(contract_root, field='largest_annual_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select code_name, date, {} from combined_largest_annual_return where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='date')
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_tr_1yr(contract_root, field='trailing_1_yr_vol'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select code_name, {} from combined_tr_1yr where code_name in {}".format(
        field, contracts), localhost, parse_dates=True)
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_ann_vol(contract_root, field='ann_vol'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select code_name, {} from combined_ann_vol where code_name in {}".format(
        field, contracts), localhost, parse_dates=True)
    return raw_df.pivot(columns='code_name', values=field)


def get_contract(contract_code, field='daily_return'):
    return pd.read_sql("select datadate, {} from futures where code_name = '{}'".format(field, contract_code), localhost, parse_dates=True, index_col='datadate')


def get_annualized_vol(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    ann_vol_cont = (contracts.std() * math.sqrt(252))
    ann_vol_sql = pd.DataFrame({'ann_vol': ann_vol_cont})
    ann_vol_sql.to_sql("combined_ann_vol", localhost,
                       if_exists='append', chunksize=250, index=True,
                       dtype={'code_name': VARCHAR(ann_vol_sql.index.get_level_values('code_name').str.len().max())})
    return ann_vol_sql


def get_trailing_1yr_vol(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    tr_1yr_vol_cont = (contracts.rolling(252).std() * math.sqrt(252)).iloc[-1]
    tr_1yr_sql = pd.DataFrame({'trailing_1_yr_vol': tr_1yr_vol_cont})
    tr_1yr_sql.to_sql("combined_tr_1yr",
                      localhost, if_exists='append', chunksize=250, index=True,
                      dtype={'code_name': VARCHAR(tr_1yr_sql.index.get_level_values('code_name').str.len().max())})
    return (contracts.rolling(252).std() * math.sqrt(252)).iloc[-1]


def get_largest_single_day_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.idxmax(),
        'largest_daily_return': contracts.max()
    })


def create_largest_daily_return_tables(contract_root):
    df = get_largest_single_day_return(contract_root).fillna(method='ffill')
    df.to_sql("combined_largest_daily_return",
              localhost, if_exists='append', chunksize=250, index=True,
              dtype={'code_name': VARCHAR(df.index.get_level_values('code_name').str.len().max())})


def get_largest_annual_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.rolling(252).sum().idxmax(),
        'largest_annual_return': contracts.rolling(252).sum().max()
    })


def create_largest_annual_return_tables(contract_root):
    df = get_largest_annual_return(contract_root).fillna(method='ffill')
    df.to_sql("combined_largest_annual_return",
              localhost, if_exists='append', chunksize=250, index=True,
              dtype={'code_name': VARCHAR(df.index.get_level_values('code_name').str.len().max())})


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
    if not layout:
        layout = _get_default_layout2(title, dtick)

    traces = []

    for field in fields:
        traces.append(go.Bar(x=df.index, y=df[field], name=field))

    fig = go.Figure(data=traces, layout=layout)
    return plot(fig, output_type=output_type)


def chart3(df, fields=None, title=None, layout=None, output_type=None, dtick='M1'):
    if not fields:
        fields = df.columns
    if not layout:
        layout = _get_default_layout3(title, dtick)

    traces = []

    for field in fields:
        traces.append(go.Bar(x=df[field], y=df[field], name=field))

    fig = go.Figure(data=traces, layout=layout)
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


def _get_default_layout2(title, dtick='M36'):
    return go.Layout(
        title=title,
        font=dict(family='Saira', size=16, color='#7f7f7f'),
        xaxis={
            'type': 'date',
            'dtick': 'M36',
            'tickmode': 'array',
            # 'tickvals': [0, 1, 2, 3],
            # 'ticktext': [title + '1', title + '2', title + '3', title + '4'],
            # 'tickformat': '%m/%y',
            # 'hoverformat': '%m/%d/%y',
            'hoverformat': 'dtick',
            'zerolinecolor': 'black',
            'showticklabels': True,
            'zeroline': True,
            'showgrid': True
        },
    )


def _get_default_layout3(title, dtick='dtick'):
    return go.Layout(
        title=title,
        font=dict(family='Saira', size=16, color='#7f7f7f'),
        xaxis={
            'type': 'category',
            'dtick': 'dtick',
            'tickmode': 'array',
            'tickvals': [0, 1, 2, 3],
            'ticktext': [title + '1', title + '2', title + '3', title + '4'],
            # 'tickformat': '%m/%y',
            # 'hoverformat': '%m/%d/%y',
            'zerolinecolor': 'black',
            'showticklabels': True,
            'zeroline': True,
            'showgrid': True
        },
    )


def chart_contracts_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root), field='px_last').fillna(method='ffill')
    return chart(df, output_type='div', title=contract_root)


def chart_returns_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='daily_return').fillna(method='ffill')
    return chart(df.cumsum(), output_type='div', title=contract_root)


def chart_ann_vol_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='ann_vol').fillna(method='ffill')
    return chart3(df, output_type='div', title=contract_root)


def chart_tr_1yr_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='tr_1yr').fillna(method='ffill')
    return chart3(df, output_type='div', title=contract_root)


def chart_daily_return_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field='largest_daily_return',
                             ).fillna(method='ffill')
    # df2 = get_contract_family('CME_{}'.format(contract_root),
    #                           field='largest_daily_return_date',
    #                           ).fillna(method='ffill')
    return chart3(df, output_type='div', title=contract_root)


def chart_annual_return_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root),
                             field=('largest_annual_return')).fillna(method='ffill')
    return chart3(df, output_type='div', title=contract_root)


def chart_dated_daily_return_dynamic(contract_root):
    df = get_contract_family_daily('CME_{}'.format(contract_root),
                                   field='largest_daily_return').fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


def chart_dated_annual_return_dynamic(contract_root):
    df = get_contract_family_annual('CME_{}'.format(contract_root),
                                    field='largest_annual_return').fillna(method='ffill')
    return chart2(df, output_type='div', title=contract_root)


if __name__ == '__main__':
    print("ANNUALIZED_VOLS")
    print (get_annualized_vol('CME_ES'))
    print (get_annualized_vol('CME_NQ'))
    print (get_annualized_vol('CME_CL'))
    print (get_annualized_vol('CME_NG'))
    print (get_annualized_vol('CME_GC'))

    print("TRAILING 1-YEAR_VOLS")
    print (get_trailing_1yr_vol('CME_ES'))
    print (get_trailing_1yr_vol('CME_NQ'))
    print (get_trailing_1yr_vol('CME_CL'))
    print (get_trailing_1yr_vol('CME_NG'))
    print (get_trailing_1yr_vol('CME_GC'))

    print("LARGEST SINGLE_DAY RETURNS")
    print (get_largest_single_day_return('CME_ES'))
    print (get_largest_single_day_return('CME_NQ'))
    print (get_largest_single_day_return('CME_CL'))
    print (get_largest_single_day_return('CME_NG'))
    print (get_largest_single_day_return('CME_GC'))

    print("LARGEST ANNUAL RETURNS")
    print (get_largest_annual_return('CME_ES'))
    print (get_largest_annual_return('CME_NQ'))
    print (get_largest_annual_return('CME_CL'))
    print (get_largest_annual_return('CME_NG'))
    print (get_largest_annual_return('CME_GC'))

    create_largest_daily_return_tables("CME_CL")
    create_largest_daily_return_tables("CME_ES")
    create_largest_daily_return_tables("CME_NQ")
    create_largest_daily_return_tables("CME_NG")
    create_largest_daily_return_tables("CME_GC")

    create_largest_annual_return_tables("CME_CL")
    create_largest_annual_return_tables("CME_ES")
    create_largest_annual_return_tables("CME_NQ")
    create_largest_annual_return_tables("CME_NG")
    create_largest_annual_return_tables("CME_GC")
