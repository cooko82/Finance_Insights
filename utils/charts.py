import matplotlib.pyplot as plt
import io
import base64

import logging
import sys

#print logging in terminal
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout 
)

def price_chart(history_df, symbol):
  """
  take the pandas df from yfinance history
  return the base64-encodeed PNG of the price chart
  """
  plt.figure(figsize=(10, 4))
  plt.plot(history_df.index, history_df["Close"])
  plt.title(f"{symbol} Closing Prices")
  plt.xlabel("Date")
  plt.ylabel("Price")
  plt.tight_layout()

  # save to memory buffer
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  buf.seek(0)
  plt.close()

  # convert to base64 so Streamlit can display it
  return base64.b64encode(buf.getvalue()).decode()
