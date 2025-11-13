"""
Copyright (c) 2025 S V SUDHARSHAN a.k.a PriceCatch.
visit http://github.com/PriceCatch.

This code is part of the PRICECATCH CHARTS project and is
licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.

Attribution:
When using this code in your project, please attribute it as follows:
- The first two lines must be placed in comments at the header of your code.
- If you are adding the code in a webpage, then, place the below phrase in the footer section
  of the webpage.
  PriceCatch Charts by S V SUDHARSHAN a.k.a PriceCatch is licensed under CC BY 4.0

- This code will fetch all five minutes bars from FYERS for current day.
- Code can be run anytime after 3.35PM before start of next trading session.
"""
import shutil
import time
from datetime import date, datetime, timedelta

import pandas as pd
from fyers_apiv3 import fyersModel
# Add the directory containing the config file to the system path
import os
import sys
config_path = "/Users/svsud/pythonprojects/all_projects_storage"
if config_path not in sys.path:
    sys.path.append(config_path)

import config
#

ACCESS_TOKEN_FILE   = config.ACCESS_TOKEN_FILE
OUTPUT_PATH         = config.minutes_5_bars_OUTPUT_PATH
INPUT_PATH          = config.minutes_5_bars_INPUT_FILE

atF = open(ACCESS_TOKEN_FILE, "r")
access_token = atF.read()
atF.close()

# FYERS 5 minutes bars folder : Remove and re-create
shutil.rmtree(OUTPUT_PATH)
os.makedirs(OUTPUT_PATH)

client_id = ""  # Replace with YOUR client ID

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

fetch_stocks = pd.read_csv(INPUT_PATH)

start_date = (input("Enter Start Date as yyyy-mm-dd: "))
end_date = (input("Enter End Date as yyyy-mm-dd: "))


def convert_to_epoch(start_date, end_date):
    # Convert input date to datetime object
    date_format     = "%Y-%m-%d"
    start_date_obj  = datetime.strptime(start_date, date_format)

    # Create two datetime objects with the specified times
    start_time      = start_date_obj.replace(hour=9, minute=15, second=0)
    _start_epoch    = int(time.mktime(start_time.timetuple()))

    end_date_obj    = datetime.strptime(end_date, date_format)
    end_time        = end_date_obj.replace(hour=15, minute=29, second=59)
    _end_epoch      = int(time.mktime(end_time.timetuple()))

    return _start_epoch, _end_epoch


start_epoch, end_epoch = convert_to_epoch(start_date, end_date)

RATE_LIMIT_PER_SECOND   = 10
RATE_LIMIT_PER_MINUTE   = 200
REQUEST_INTERVAL        = 1 / RATE_LIMIT_PER_SECOND
REQUESTS_PER_MINUTE     = 200


def fetch_ohlc(symbol):
    # Prefix "NSE:" and suffix "-EQ"
    symbol_with_prefix_suffix = 'NSE:' + symbol + '-EQ'

    data = {
        "symbol"     : symbol_with_prefix_suffix,
        "resolution" : "5",
        "date_format": "0",
        "range_from" : start_epoch,
        "range_to"   : end_epoch,
        "cont_flag"  : "1"
    }

    response = fyers.history(data=data)
    if response["s"] == "ok":
        # Convert the data to a DataFrame
        columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df      = pd.DataFrame(response['candles'], columns=columns)
        _file   = f"{OUTPUT_PATH}/{symbol.upper()}.csv"

        df.to_csv(_file, index=False)


# Extract unique symbols
symbols = fetch_stocks['Symbol'].unique()
# Prefix "NSE:" and suffix "-EQ"
symbols_with_prefix_suffix = ['NSE:' + Symbol + '-EQ' for Symbol in symbols]

start_time = time.time()
for i, symbol in enumerate(symbols):
    if i % RATE_LIMIT_PER_SECOND == 0:
        time.sleep(REQUEST_INTERVAL)
    if i % REQUESTS_PER_MINUTE == 0 and i != 0:
        elapsed = time.time() - start_time
        if elapsed < 60:
            time.sleep(60 - elapsed)
        start_time = time.time()
    fetch_ohlc(symbol)

print("Done.")
