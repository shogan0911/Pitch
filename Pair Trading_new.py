import pandas as pd
import requests
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
#%%

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
# %%

e = 0
q = 0
most_days = []

for q in range(len(company_by_naics_code)):

    for e in range(len(company_by_naics_code[q])):

        ticker_ph = company_by_naics_code[q][e]
        max_days = len(final[q][ticker_ph])

    most_days.append(max_days)
max(most_days)
#%%
ticker_trading_days = final
ticker_symbol_ph = []
ticker_symbol = []

for q in range(len(company_by_naics_code)):

    for e in range(len(company_by_naics_code[q])):

        ticker_ph = company_by_naics_code[q][e]

        if len(final[q][ticker_ph]) == max(most_days):
            ticker_symbol_ph.append(ticker_ph)

        if len(final[q][ticker_ph]) < max(most_days):
            del ticker_trading_days[q][ticker_ph]

    ticker_symbol.append(ticker_symbol_ph)
    ticker_symbol_ph = []





#%%
i = 0

#%%

test = ([ticker_symbol[0][0]] * (len(ticker_symbol[0])))
#%%

for c in range(len(ticker_trading_days)):

    for t in range(len(test)):

        test = [ticker_symbol[c][0]] * len(ticker_symbol[c])

        p = test[t]
        f = ticker_symbol[c][t]

        res = sm.OLS(ticker_trading_days[c][p], ticker_trading_days[c][f])
        result = res.fit()
        result.summary()
#%%
    test = [ticker_symbol[c][0]] * len(ticker_symbol[c])
#%%


    res = sm.OLS(ticker_trading_days[c]['AR'], ticker_trading_days[c]['APA'])
    result = res.fit()
    d = result.resid
#%%

ts.adfuller(d)

#%%
print(ticker_symbol[c][0])
print(len(ticker_symbol[c]))
print(p)
print(f)
print(t)
print(ticker_symbol[1][0])
