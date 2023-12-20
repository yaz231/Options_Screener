from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
import bs4 as bs
import requests
import re
import json
import pandas as pd
import bisect
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import yfinance as yf
from yahoo_fin import options as op, stock_info as si

global_df = pd.DataFrame(
    columns=['Symbol', 'Strike', 'Type', 'Last Trade Price', 'Bid', 'Ask', 'Open Interest', 'Volume',
             'Short Profit Chance',
             'Long Profit Chance', 'Delta', 'Volatility', 'Theta'])


def find_expiration(week=0):
    today = datetime.today()
    days_to_friday = (4 - today.weekday()) % 7
    expiration_date = (today + timedelta(days=days_to_friday + 7 * week)).strftime('%Y-%m-%d')
    return expiration_date


def find_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    tickers = [s.replace('\n', '') for s in tickers]
    return tickers


def create_df(type='put', week=0):
    tickers = si.tickers_sp500()

    dfs = []

    def worker(ticker_list):
        local_dfs = []
        for ticker in ticker_list:
            try:
                if type == 'put':
                    local_dfs.append(reformat_df(op.get_puts(ticker, find_expiration(week))))
                else:
                    local_dfs.append(reformat_df(op.get_calls(ticker, find_expiration(week))))
            except ImportError:
                print(f"No options data available for {ticker}. Skipping...")
                continue

        dfs.extend(local_dfs)

    num_threads = 10
    ticker_lists = [tickers[i::num_threads] for i in range(num_threads)]
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(ticker_lists[i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    df = pd.concat(dfs, ignore_index=True)
    df['Ratio'] = (df['Last Price'] / df['Strike']) * 100
    df.to_csv(f'options_{type}_data.csv', index=False)

    return df


def filter_stock_data():
    df = pd.read_csv('options_data.csv')

    return


def find_atm_options(type='put'):
    tickers = si.tickers_sp500()
    df = pd.read_csv(f'options_{type}_data.csv')

    dfs = []  # create empty list to hold filtered options for all tickers

    def worker(ticker_list):
        local_dfs = []
        for ticker in ticker_list:
            if ticker not in df['Symbol'].unique():
                continue
            current_price = si.get_live_price(ticker)
            temp_df = df[df['Symbol'] == ticker]
            idx = bisect.bisect_left(temp_df['Strike'].to_numpy(), current_price)
            if type == 'put':
                filtered_options = temp_df.iloc[idx: idx + 5]
            else:
                filtered_options = temp_df.iloc[idx - 5: idx]

            # add filtered options to results list
            local_dfs.append(filtered_options)

        dfs.extend(local_dfs)

    num_threads = 10
    ticker_lists = [tickers[i::num_threads] for i in range(num_threads)]
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(ticker_lists[i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(f'options_{type}_atm_data.csv', index=False)

    return final_df


def reformat_df(df):
    df.insert(0, 'Symbol', re.search(r'\D+', df['Contract Name'].iloc[0]).group())
    df = df.drop(columns=["Contract Name", "Last Trade Date"])
    return df


def insert_into_df(df, index, column_name, value):
    df.insert(index, column_name, value)
    df1 = df.iloc[:, :index]
    df2 = df.iloc[:, index:]
    final_df = pd.concat([df1, df1.pop(column_name), df2], axis=1)
    return final_df


pd.set_option('display.max_columns', None)

# print(rs.login(user, pwd)['detail'])
# print(create_global_dataframe(type='put'))
# df = get_stock_data('TSLA')
columns = ['symbol', 'current_price', 'strike', 'exp_date', 'premium', 'open_interest', 'implied_volatility']

# df = pd.read_csv('sample_option_chain.csv')
df = reformat_df(op.get_puts('TSLA', find_expiration()))
# print(df['symbol'])
current_price = si.get_live_price(df['Symbol'].iloc[0])
df.insert(1, "current_price", current_price)
df.insert(3, 'exp_date', find_expiration())
df = df.drop(columns=['Bid', 'Ask', 'Change', '% Change', 'Volume'])
df = df.rename(columns=dict(zip(df.columns, columns)))


print(df.columns)

# create_df()
# print(find_atm_options())


#
# # RUN 'uvicorn main:app --reload'
# app = FastAPI()
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# class UserCredentials(BaseModel):
#     username: str
#     password: str
#
# @app.post("/login")
# async def authenticate_user(user: UserCredentials):
#     rs.login(username=user.username, password=user.password)
#
#     return {"message": "Account Authenticated"}
#
# @app.get("/all_data")
# async def authenticate_user(user: UserCredentials):
#     today = datetime.today()
#     days_to_friday = (4 - today.weekday()) % 7
#     expiration_date = (today + timedelta(days=days_to_friday)).strftime('%Y-%m-%d')
#     print(expiration_date)
#     tickers = find_sp500_tickers()
#     df = pd.DataFrame(
#         columns=['Symbol', 'Strike', 'Type', 'Bid', 'Ask', 'Open Interest', 'Volume', 'Short Profit Chance',
#                  'Long Profit Chance', 'Delta', 'Volatility', 'Theta'])
#
#     columns = ['Symbol', 'Strike', 'Type', 'Bid', 'Ask', 'Open Interest', 'Volume', 'Short Profit Chance',
#                'Long Profit Chance', 'Delta', 'Volatility', 'Theta']
#
#     keys_to_select = ['symbol', 'strike_price', 'type', 'bid_price', 'ask_price', 'open_interest', 'volume',
#                       'chance_of_profit_short',
#                       'chance_of_profit_long', 'delta', 'implied_volatility', 'theta']
#
#     dfs = []
#     for ticker in tickers[:10]:
#         options = rs.find_options_by_expiration(inputSymbols=ticker, expirationDate=expiration_date, optionType='put')
#         if len(options) == 0: continue
#
#         options_data = [{k: option[k] for k in keys_to_select} for option in options]
#         # print(options_data)
#         options_df = pd.DataFrame(options_data)
#         # print(options_df)
#         dfs.append(options_df)
#
#     df = pd.concat(dfs, ignore_index=True)
#
