import quandl
import pandas as pd
import quandl.errors.quandl_error as quandl_error
from sqlalchemy import create_engine
import math

quandl.ApiConfig.api_key = 'Np-ijpp9HVJju6Kgtbia'

localhost = create_engine('mysql://root:password@localhost/solution')


def pull_data(code_name, start='2005-01-01'):
    try:
        print ("Pulling data for: {}".format(code_name))
        res = quandl.get('CHRIS/{}'.format(code_name), start=pd.to_datetime((start)))
    except quandl_error.NotFoundError:
        print ("Bad Quandl code: {}".format(code_name))
        return

    res['daily_return'] = res['Settle'] / res['Settle'].shift(1) - 1.
    res['code_name'] = code_name
    res['ann_vol'] = res['daily_return'].std() * math.sqrt(252)
    res['tr_1yr'] = (res['daily_return'].rolling(252).std() * math.sqrt(252)).iloc[-1]
    res['largest_daily_return'] = res['daily_return'].max()
    res['largest_daily_return_date'] = res['daily_return'].idxmax()
    res['largest_annual_return'] = res['daily_return'].rolling(252).sum().max()
    res['largest_annual_return_date'] = res['daily_return'].rolling(252).sum().idxmax()

    to_save = res[['code_name', 'Settle', 'daily_return', 'ann_vol', 'tr_1yr',
                   'largest_daily_return', 'largest_daily_return_date',
                   'largest_annual_return', 'largest_annual_return_date']].rename(columns={
                       'Settle': 'px_last'})
    to_save.index.name = 'datadate'

    return to_save


# df_daily = pull_data().iloc[:, [0, 5, 6]]
# print(df_daily.head(10))


def run():
    dfs = []
    for code_root in ['CME_CL', 'CME_NQ', 'CME_ES', 'CME_NG', 'CME_GC']:
        for contract_number in range(1, 5):
            dfs.append(pull_data('{}{}'.format(code_root, contract_number)))
    full_df = pd.concat(dfs)
    full_df.to_sql('futures', localhost, if_exists='replace', chunksize=250)
    return full_df


if __name__ == '__main__':
    run()
