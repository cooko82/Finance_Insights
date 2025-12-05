
import logging
import datetime as dt

import sys
import yfinance as yf
import pandas as pd

#print logging in terminal
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout 
)

def fetch_info(ticker: str):
  """fetch gen info about stock. return things: company name, market cap, P?E ratio, live price (if ava)
  args: ticker(str): stock symbol like AAPL
  return: info provided by yahoo finance. in dict form
  """
  ticker = ticker.upper().strip() #make upper and remove any white space
  stock = yf.Ticker(ticker)

  if stock.info != None:
    logging.info(f"Returning info about {ticker}")
    return stock.info
  else:
    logging.info(f"No info about {ticker} available")
    return None

def fetch_history(ticker: str, period: str):
  """fetch price history for a stock
  example inputs: 1d, 5d, 1mo, 1y, 2y, max
  
  input 
  ticker = stock symbol
  period = time period requested

  returns pd dataframe or None
  """
  ticker = ticker.upper().strip()
  stock = yf.Ticker(ticker)

  df = stock.history(period)
  if df.empty == False:
    logging.info(f"Returning history about {ticker}")
    return df
  
  else:
    logging.info(f"No history about {ticker} available")
    return None


def fetch_live_price(ticker: str):
  """attempt to get live current price
  1. try reading from info['regularMarketPrice']
  2. try the last close from today's data

  input: ticker
  output: flaot or None for the latest price
  """

  info_dict = fetch_info(ticker)

  if "regularMarketPrice" in info_dict:
    logging.info("regularMarketPrice found in info_dict")
    return float(info_dict["regularMarketPrice"])
  elif "currentPrice" in info_dict:
    logging.info("currentPrice found in info_dict")
    return float(info_dict["currentPrice"])

  #if the price is not in the info_dict we will fetch history and check the day's last close
  hist_df = fetch_history(ticker, period="1d")

  if hist_df.empty == False:
    #TODO this part doesnt work as expected fix it
    price = float(hist_df["Close"].iloc[-1])
    logging.info("Closing price from fetch_history")
    return price
  logging.info("No current price available")
  return None

def fetch_key_metrics(ticker:str):
  """
  Return the most useful key metrics

  input ticker
  output selected fields as dict
  """

  info_dict = fetch_info(ticker)

  try:
    key_stock_dict = {
      "symbol": info_dict.get("symbol"),
      "name": info_dict.get("shortName"),
      "price": info_dict.get("regularMarketPrice"),
      "previous_close": info_dict.get("previousClose"),
      "market_cap": info_dict.get("marketCap"),
      "pe_ratio": info_dict.get("trailingPE"),
      "eps": info_dict.get("epsTrailingTwelveMonths"),
      "dividend_yield": info_dict.get("dividendYield"),
    }
    return key_stock_dict
  except Exception as e:
    logging.info(f"Error getting key_stock_dict: {e}")

def fetch_news(ticker):
  """
  fetch recent news articles for the stock

  input ticker
  return dict with news
  """
  ticker = ticker.upper().strip()
  stock = yf.Ticker(ticker)

  news = stock.news
  if len(news) > 0:
    logging.info(f"{ticker} news found")
    return {f"{ticker} news": news}
  logging.info(f"{ticker} no news found")
  return {f"{ticker} news": []}

def fetch_ticker_summary(ticker:str):
  """
  high level convenience function

  bundles together
  - key fin metrics
  - live price
  - historial data
  - recent news
  """

  stock_summary_dict = {}

  key_metrics_dict = fetch_key_metrics(ticker)
  #add metrics to stock_summary_dict
  stock_summary_dict.update(key_metrics_dict)

  stock_summary_dict["live_price"] = fetch_live_price(ticker)
  # stock_summary_dict["history"] = fetch_history(ticker, period)
  #stock_summary_dict.update(fetch_news(ticker))

  logging.info(f"{ticker} returning stock summary dict")
  return stock_summary_dict


#Testing
ticker = "TSLA"
print(fetch_info("CBA"))
print(fetch_history("CBA", "1d"))
print(fetch_live_price("TSLA"))
print(fetch_key_metrics(ticker))
print(fetch_news(ticker))
print(fetch_ticker_summary(ticker))

