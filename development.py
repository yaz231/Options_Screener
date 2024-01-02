import os
from yahoo_fin import options as op, stock_info as si, news as nws
import yfinance as yf

print(op.get_calls('TSLA').columns)

# print(si.get_analysts_info("NFLX"))
# print(si.get_balance_sheet('TSLA'))                               ##NOT WORKING
# print(si.get_cash_flow('tsla', yearly=True))                      ##NOT WORKING
# print(si.get_company_info('TSLA'))                                ##NOT WORKING

# print(si.get_currencies())
# print(si.get_data("TSLA"))
# print(si.get_day_gainers())
# print(si.get_day_losers())
# print(si.get_day_most_active())
# print(si.get_dividends("AAPL"))
# print(si.get_earnings("NFLX"))                                    ##NOT WORKING
# print(si.get_earnings_for_date("02/08/2021"))                     ##NOT WORKING
# print(si.get_earnings_in_date_range('02/08/2021', '02/12/2021'))  ##NOT WORKING
# print(si.get_earnings_history("TSLA"))                            ##NOT WORKING
# print(si.get_financials("TSLA"))                                  ##NOT WORKING
# print(si.get_futures())
# print(si.get_holders("TSLA"))
# print(si.get_income_statement("TSLA"))                            ##NOT WORKING
# print(si.get_live_price("TSLA"))
# print(si.get_market_status())                                     ##NOT WORKING
# print(si.get_next_earnings_date("TSLA"))                          ##NOT WORKING
# get_premarket_price
# get_postmarket_price
# get_quote_data
# get_quote_table
# get_top_crypto
# get_splits
# get_stats
# get_stats_valuation
# get_undervalued_large_caps
# tickers_dow
# tickers_ftse100
# tickers_ftse250
# tickers_ibovespa
# tickers_nasdaq
# tickers_nifty50
# tickers_niftybank
# tickers_other
# print(si.tickers_sp500(True))

msft = yf.Ticker("MSFT")

# get all stock info
# print(msft.info)

# # get historical market data
# hist = msft.history(period="1mo")
#
# # show meta information about the history (requires history() to be called first)
# print(msft.history_metadata)

# # show actions (dividends, splits, capital gains)
# print(msft.actions)
# print(msft.dividends)
# print(msft.splits)
# print(msft.capital_gains)  # only for mutual funds & etfs
#
# # show share count
# print(msft.get_shares_full(start="2022-01-01", end=None))
#
# # show financials:
# # - income statement
# print(msft.income_stmt)
# print(msft.quarterly_income_stmt)
# # - balance sheet
# print(msft.balance_sheet)
# print(msft.quarterly_balance_sheet)
# # - cash flow statement
# print(msft.cashflow)
# print(msft.quarterly_cashflow)
# # see `Ticker.get_income_stmt()` for more options
#
# # show holders
# print(msft.major_holders)
# print(msft.institutional_holders)
# print(msft.mutualfund_holders)
#
# # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
# # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
# print(msft.earnings_dates)
#
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# print(msft.isin)
#
# # show options expirations
# print(msft.options)
#
# # show news
# print(msft.news)
#
# # get option chain for specific expiration
# opt = msft.option_chain('YYYY-MM-DD')
# # data available via: opt.calls, opt.puts
