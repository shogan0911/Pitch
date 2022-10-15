import itertools
import pandas as pd
import requests
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

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
            'https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/day/2021-10-10/2022-10-10?adjusted=true&sort=asc&apiKey=x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3').json()

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

# (Probably not the most effective method) Because I need to make combinations of the various stock tickers for the
# ADF test, I determine what stocks are still in "ticker_trading_days" and copy the stock tickers and keep them
# seperated by NAICS code. I then create the combinations and put them in a nested list. After that, the stock daily
# prices are combined with their respective stocks.

a_ph = []
a = []

for i in range(len(company_by_naics_code)):
    for k in range(len(company_by_naics_code[i])):

        if company_by_naics_code[i][k] in ticker_trading_days[i]:
            a_ph.append(company_by_naics_code[i][k])
    a.append(a_ph)
    a_ph = []



#%%
permutations = []

for i in range(len(a)):

    q = list(itertools.permutations(a[i], 2))
    permutations.append(q)


p = []
p_ph = []
for i in range(len(permutations)):
    for k in range(len(permutations[i])):
        for t in range(len(permutations[i][k])):

            p_ph.append(permutations[i][k][t])
        p.append(p_ph)
        p_ph = []


#%%

o = []
o_ph = []
for y in range(len(permutations)):
    for t in range(len(permutations[y])):
        for r in range(len(permutations[y][t])):
            o_ph.append(ticker_trading_days[y][permutations[y][t][r]])
        o.append(o_ph)
        o_ph = []

df = pd.DataFrame((p, o)).transpose()


#%%

f = 0
g = []

while f <= len(df.iloc[:, 0]) - 1:
    s = (df.iloc[f, 1])[0]
    s1 = (df.iloc[f, 1][1])
    print(s)
    print(s1)

    a = sm.OLS(s, s1)
    e = a.fit()
    t = list(e.resid)

    g.append(t)

    f = f + 1

#%%

passed = []

df_ph = pd.DataFrame(df.iloc[:, 0])
g_ph = pd.DataFrame(g)
df_residuals = pd.concat([df_ph, g_ph], axis=1, ignore_index='True')


#%%

for i in range(len(df_residuals.iloc[:, 0])):
    n = ts.adfuller(df_residuals.iloc[i, 1:])

    if n[0] < n[4]['5%']:

        passed.append('Passed')
        print('Passed')

    else:
        passed.append('Failed')
        print('Failed')


#%%

df_pass_fail_ph = pd.DataFrame(passed)
df_pass_fail = pd.concat([df_ph, df_pass_fail_ph], axis=1, ignore_index='True').rename(columns={0: 'Pair', 1: 'Status'})

superior_pass_df = df_pass_fail.loc[df_pass_fail['Status'] == 'Passed']
superior_pass_df = superior_pass_df.sort_values(by=['Pair']).reset_index(drop='True')

excel_superior_pass_df = pd.DataFrame(superior_pass_df['Pair'].to_list(), columns=['Stock A', 'Stock B'])
excel_superior_pass_df = pd.concat([excel_superior_pass_df, superior_pass_df['Status']], axis=1)


#%%
excel_superior_pass_df.to_excel('Pair_Trade_Candidates.xlsx', index='False')

#%%

south_west = requests.get('https://api.polygon.io/v2/aggs/ticker/LUV/range/1/day/2021-10-10/2022-10-10?'
                          'adjusted=true&sort=asc&limit=5000&apiKey=x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3').json()

south_west_close = []
for x in range(len(south_west['results'])):
    south_west_close_ph = south_west['results'][x]['c']
    south_west_close.append(south_west_close_ph)

#%%

delta = requests.get('https://api.polygon.io/v2/aggs/ticker/DAL/range/1/day/2021-10-10/2022-10-10?'
                          'adjusted=true&sort=asc&limit=5000&apiKey=x4kfbN2sNWrGtNGbEQT8ORSlLfxoSkx3').json()

delta_close = []
for x in range(len(delta['results'])):
    delta_close_ph = delta['results'][x]['c']
    delta_close.append(delta_close_ph)


#%%

hedge = sm.OLS(south_west_close, delta_close)
hedge_r = hedge.fit()
print(hedge_r.summary())

#%%

hedge = sm.OLS(delta_close, south_west_close)
hedge_r = hedge.fit()
print(hedge_r.summary())