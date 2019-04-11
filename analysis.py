import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib  # noqa
from sqlalchemy import create_engine
import math
import matplotlib  # noqa
matplotlib.use('PS')  # noqa
from plotly.offline import plot
import plotly.figure_factory as ff
import plotly.graph_objs as go

localhost = create_engine('mysql://root:password@localhost/solution')


def get_contract_family(contract_root, field='daily_return'):
    contracts = '({})'.format(
        ','.join(["'{}{}'".format(contract_root, contract_no) for contract_no in range(1, 5)]))
    raw_df = pd.read_sql("select datadate, code_name, {} from futures where code_name in {}".format(
        field, contracts), localhost, parse_dates=True, index_col='datadate')
    return raw_df.pivot(columns='code_name', values=field)


def get_contract_family_returns(contract_root):
    # When working with financial data, we handle 'missing values' depending on the type of data we are working with.
    # A rule of thumb is, when dealing with % returns, we replace missing data with 0
    return get_contract_family(contract_root, field='daily_return').replace(np.nan, 0)


def get_contract_family_prices(contract_root):
    # And for prices, we FORWARD FILL, IE, push the previous days price, forward.  IF we replaced with 0s, think about how crazy the price chart would look (ie 95, 96, 0, 96.5)
    return get_contract_family(contract_root, field='px_last').fillna(method='ffill')


def get_contract(contract_code, field='daily_return'):
    return pd.read_sql("select datadate, {} from futures where code_name = '{}'".format(field, contract_code), localhost, parse_dates=True, index_col='datadate')


def get_annualized_vol(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return contracts.std() * math.sqrt(252)


def get_trailing_1yr_vol(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    # return (contracts.rolling(252).std() * math.sqrt(252)).iloc[-1]
    tr_1yr_vol_cont = (contracts.rolling(252).std() * math.sqrt(252)).iloc[-1]
    tr_1yr_vol_cont.to_csv("%s_tr_1yr_vol.csv" % (contract_root))
    return tr_1yr_vol_cont


def get_largest_single_day_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.idxmax(),
        'largest_daily_return': contracts.max()
    })


def create_largest_daily_return_tables(contract_root):
    df = get_largest_single_day_return(contract_root).fillna(method='ffill')
    df.to_csv(contract_root + "_largest_daily_return.csv")


def get_largest_annual_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.rolling(252).sum().idxmax(),
        'largest_annual_return': contracts.rolling(252).sum().max()
    })


def create_largest_ann_return_tables(contract_root):
    df = get_largest_annual_return(contract_root).fillna(method='ffill')
    df.to_csv(contract_root + "_largest_ann_return.csv")


def pretty_plot(df, fields=[], figsize=(35, 10), title="Title", loc=2, hline=False, ylabel='Returns'):
    if not fields:
        fields = df.columns.values
    plt.figure(figsize=figsize, dpi=80)
    for cback in fields:
        plt.plot(df[cback], linewidth='0.7', label=cback)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc=loc)
    if hline:
        plt.axhline(0, linewidth='1.5', color='black')
    plt.gca().grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.gca().grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    plt.minorticks_on()
    plt.show()


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


def chart_returns_dynamic(df, fields=None, title=None, layout=None, output_type=None, dtick='M1'):
    if not fields:
        fields = df.columns
    if not layout:
        layout = _get_default_layout(title, dtick)

    traces = []

    for field in fields:
        traces.append(go.Scattergl(x=df.index, y=df[field], mode='lines', name=field))

    fig = go.Figure(data=traces, layout=layout)
    return plot(fig, output_type=output_type)


def chart_contract(code_name):
    df = get_contract(code_name, field='px_last').fillna(method='ffill')
    pretty_plot(df, title=code_name, ylabel='px_last')


def chart_contracts(contract_root):
    df = get_contract_family(contract_root, field='px_last').fillna(method='ffill')
    pretty_plot(df, title=contract_root, ylabel='px_last')
    print(df.head())


def chart_contracts_dynamic(contract_root):
    df = get_contract_family('CME_{}'.format(contract_root), field='px_last').fillna(method='ffill')
    return chart(df, output_type='div', title=contract_root)


def create_tables(contract_root):
    df = get_contract_family(contract_root, field='px_last').fillna(method='ffill')
    df.to_sql(contract_root, localhost, if_exists='replace', chunksize=250)


def create_returns_tables(contract_root):
    df = get_contract_family(contract_root, field='daily_return').fillna(method='ffill')
    df.to_sql(contract_root + "_ret", localhost, if_exists='replace', chunksize=250)
    print (df.head())
    df.cumsum().to_sql(contract_root + "_cumsum", localhost, if_exists='replace', chunksize=250)


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

    create_tables("CME_CL")
    create_tables("CME_ES")
    create_tables("CME_NQ")
    create_tables("CME_NG")
    create_tables("CME_GC")

    create_returns_tables("CME_CL")
    create_returns_tables("CME_ES")
    create_returns_tables("CME_NQ")
    create_returns_tables("CME_NG")
    create_returns_tables("CME_GC")

    create_largest_daily_return_tables("CME_CL")
    create_largest_daily_return_tables("CME_ES")
    create_largest_daily_return_tables("CME_NQ")
    create_largest_daily_return_tables("CME_NG")
    create_largest_daily_return_tables("CME_GC")

    create_largest_ann_return_tables("CME_CL")
    create_largest_ann_return_tables("CME_ES")
    create_largest_ann_return_tables("CME_NQ")
    create_largest_ann_return_tables("CME_NG")
    create_largest_ann_return_tables("CME_GC")
