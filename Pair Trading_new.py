import itertools

import pandas as pd
import requests
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
from itertools import permutations
#%%
# The specific stocks are being read from "pair_trade_data.csv" into a DataFrame.
# The stocks are then grouped by NAICS code.

screened_stock_data = pd.read_csv('C:\\Users\\scteh\\OneDrive\\Desktop\\pair_trade_data.csv')
grouped_by_naics_code = screened_stock_data.groupby('NAICS Industry Codes')['Ticker'].apply(list)
grouped_by_naics_code.reset_index(name='NAICS Industry Code')

# The companies sorted by their NAICS code are then filtered. NAICS codes with less than
# four companies are excluded from the program.

company_by_naics_code = []

for i in range(len(grouped_by_naics_code)):
    x = grouped_by_naics_code.iloc[i]

    if len(grouped_by_naics_code.iloc[i]) >= 4:
        company_by_naics_code.append(x)

#%%

# Within each NAICS group, the daily close price of each stock within that NAICS group
# is pulled from Polygon.io. A dictionary is then created by separating every group by NAICS code,
# and then by individual stock. The daily close prices are then connected to each individual stock.

ticker_data_dict = {}
daily_close_by_ticker = []
price_data = []
final = {}

for q in range(len(company_by_naics_code)):

    print('Group ' + str(q))

    for e in range(len(company_by_naics_code[q])):

        ticker = company_by_naics_code[q][e]
        stock_price_data = requests.get(
            'https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/day/2020-09-28/2022-09-30?adjusted=true&sort=asc&apiKey=x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3').json()

        for i in range(len(stock_price_data['results'])):
            daily_close = stock_price_data['results'][i]['c']
            daily_close_by_ticker.append(daily_close)

        ticker_data_dict[company_by_naics_code[q][e]] = daily_close_by_ticker
        daily_close_by_ticker = []

        print(ticker)

    final[q] = ticker_data_dict
    ticker_data_dict = {}


#%%

# Since not all stocks contain the same amount of daily data, we now determine which stock has the most trading days.

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

# After the number of trading days is determined, we then sort out all the stocks that have less than that number
# of trading days. Those sorted stocks are then deleted.

ticker_trading_days = final
ticker_symbol_ph = []

for q in range(len(company_by_naics_code)):

    for e in range(len(company_by_naics_code[q])):

        ticker_ph = company_by_naics_code[q][e]

        if len(final[q][ticker_ph]) == max(most_days):
            ticker_symbol_ph.append(ticker_ph)

        if len(final[q][ticker_ph]) < max(most_days):
            del ticker_trading_days[q][ticker_ph]

    ticker_symbol_ph = []




#%%

a_ph = []
a = []

for i in range(len(company_by_naics_code)):
    for k in range(len(company_by_naics_code[i])):

        if company_by_naics_code[i][k] in ticker_trading_days[i]:
            a_ph.append(company_by_naics_code[i][k])
    a.append(a_ph)
    a_ph = []

#%%


q = list(itertools.permutations(a[0], 2))

#%%

p = []
p_ph = []
for i in range(len(q)):
    for k in range(len(q[i])):
        p_ph.append(q[i][k])
    p.append(p_ph)
    p_ph = []


#%%

o = []
o_ph = []
for t in range(len(p)):
    for r in range(len(p[t])):
        o_ph.append(ticker_trading_days[0][p[t][r]])
    o.append(o_ph)
    o_ph = []
#%%

df = pd.DataFrame((p, o)).transpose()

#%%

f = 0
g = []

while f<= len(df.iloc[:,0])-1:
    s = (df.iloc[f,1])[0]
    s1 = (df.iloc[f,1][1])
    print(s)
    print(s1)

    a = sm.OLS(s, s1)
    e = a.fit()
    t = list(e.resid)



    g.append(t)

    f = f + 1






#%%

print(s)