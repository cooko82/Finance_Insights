from utils.data_fetcher import fetch_history
from utils.charts import price_chart
import base64
import logging
import sys

#print logging in terminal
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout 
)


ticker = "TSLA"
#fetch sample data
df = fetch_history(ticker, period="1y")

#generate chart as base64 string
img_64 = price_chart(df, ticker)

#save output to an image file to see if worked
with open("test_chart.png", "wb") as file:
  file.write(base64.b64decode(img_64))

logging.info("Chart saved as test_chart")
