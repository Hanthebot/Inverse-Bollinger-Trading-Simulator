import yfinance as yf
import csv
import datetime

def crawl_ticker(ticker: str, starting: str, ending: str, interval: str = "1d", prefix: str = "", suffix: str = ""):
    """
    Crawls the historical data of a given ticker from Yahoo Finance and saves it to a CSV file.

    Args:
        ticker (str): The ticker symbol of the stock.
        starting (str): The starting date of the historical data in the format 'YYYY-MM-DD'.
        ending (str): The ending date of the historical data in the format 'YYYY-MM-DD'.
        interval (str, optional): The interval of the data (e.g., '1d' for daily, '1h' for hourly). Defaults to '1d'.
    """
    # Create a Ticker object from yfinance library
    data = yf.download(ticker, starting, ending, auto_adjust=False)
    
    data.to_csv(f'data/{prefix}{ticker}_{starting}_{ending}{suffix}.csv')

def crawl_all(csv_path: str, format="%Y-%m-%d"):
    data = []
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    for dat in data:
        crawl_ticker(dat["Company"], \
            (datetime.datetime.strptime(dat["Date"], format)-datetime.timedelta(days=2*30/5*7)).strftime("%Y-%m-%d"), \
            (datetime.datetime.strptime(dat["Date"], format)+datetime.timedelta(days=2*30/5*7)).strftime("%Y-%m-%d"), \
            suffix = f"_{dat['Date']}_{dat['Expected Sign']}_{dat['Phase']}")
        print(f"Finished {dat['Company']}_{dat['Date']}")