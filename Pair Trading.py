import pandas as pd
import numpy as np
import json
import requests

api_key = 'x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3'

screened_stock_data = pd.read_csv('C:\\Users\\scteh\\OneDrive\\Desktop\\pair_trade_data.csv')

grouped_by_naics_code = screened_stock_data.groupby('NAICS Industry Codes')['Ticker'].apply(list)

grouped_by_naics_code.reset_index(name='NAICS Industry Code')


#%%

company_by_naics_code = []
for i in range(len(grouped_by_naics_code)):
    x = grouped_by_naics_code.iloc[i]

    if len(grouped_by_naics_code.iloc[i]) >= 4:
        company_by_naics_code.append(x)

#%%

ticker_data_dict = {}
daily_close_by_ticker = []
price_data = []
final = {}


for q in range(len(company_by_naics_code)):

    for e in range(len(company_by_naics_code[q])):

        ticker = company_by_naics_code[q][e]
        stock_price_data = requests.get(
            'https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/day/2022-09-28/2022-09-30?adjusted=true&sort=asc&apiKey=x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3').json()

        for i in range(len(stock_price_data['results'])):
            daily_close = stock_price_data['results'][i]['c']
            daily_close_by_ticker.append(daily_close)

        ticker_data_dict[company_by_naics_code[q][e]] = daily_close_by_ticker
        daily_close_by_ticker = []

    final[q] = ticker_data_dict
    ticker_data_dict = {}
    print(q)

#%%
