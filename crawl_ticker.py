import yfinance as yf

def crawl_ticker(ticker: str, starting: str, ending: str, interval: str = "1d"):
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
    
    data.to_csv(f'data/{ticker}_{starting}_{ending}.csv')
