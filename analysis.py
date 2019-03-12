import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
import math
import matplotlib  # noqa
#matplotlib.use('PS')  # noqa
import matplotlib



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
    return (contracts.rolling(252).std() * math.sqrt(252)).iloc[-1]


def get_largest_single_day_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.idxmax(),
        'largest_daily_return': contracts.max()
    })


def get_largest_annual_return(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    return pd.DataFrame({
        'date': contracts.rolling(252).sum().idxmax(),
        'largest_annual_return': contracts.rolling(252).sum().max()
    })


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


def chart_contract(code_name):
    df = get_contract(code_name, field='px_last').fillna(method='ffill')
    pretty_plot(df, title=code_name, ylabel='px_last')


def chart_contracts(contract_root):
    df = get_contract_family(contract_root, field='px_last').fillna(method='ffill')
    pretty_plot(df, title=contract_root, ylabel='px_last')


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

    chart_contracts("CME_CL")
