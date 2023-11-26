import datetime
from glob import glob
import csv
import re
import backtrader as bt
from scipy import stats
import matplotlib.pyplot as pl
pl.style.use("default") #ggplot is also fine
pl.rcParams["figure.figsize"] = (12,7)

from strategy import inverse_bollinger, bollinger, sma

def sigma_to_frequency(sigma: float, duration: int):
    """
    Return order size - total value ratio based on trade number estimation
    """
    probability = 2*stats.norm.cdf(-sigma) # probability of execution
    return min(1/(duration * probability), 1.00)

def find_init_fin(datafile: str, fromdate, todate):
    """
    Find initial and final closing price from datafile, within fromdate and todate - both inclusive
    """
    with open(datafile, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        open_close = []
        prev_row4 = 1
        prev_date = datetime.datetime(1,1,1,0,0).date()
        for row in reader:
            date = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
            if prev_date < fromdate.date() and date >= fromdate.date():
                init_close = float(row[4])
            if prev_date <= todate.date() and date > todate.date():
                fin_close = prev_row4
            prev_date = date
            prev_row4 = float(row[4])
        return (init_close, fin_close)

def regex_process(datafiles: list):
    """
    extracts and returns useful information from file names, as well as simplified name
    """
    # capture ticker, release date, result, and stage from filename
    pattern = r"\./data\\(.+)_[\d-]+_[\d-]+_([\d-]+)_(.+)_(\d).csv"
    replacement_pattern = r"\1_\2_\3_\4"
    simple_names = [re.sub(pattern, replacement_pattern, datafile) for datafile in datafiles]
    meta_data = [list(re.findall(pattern, datafile)[0]) for datafile in datafiles]
    return (meta_data, simple_names)

def stock_data_init(datafile: str, key_date: str, period, data_output:dict):
    """
    Returns Backtester-formatted data, also adds long and short to data_output dict
    """
    # Create a Data Feed
    fromdate = datetime.datetime.strptime(key_date, "%Y-%m-%d")-period
    todate = datetime.datetime.strptime(key_date, "%Y-%m-%d")+period
    data = bt.feeds.GenericCSVData(
        dataname=datafile,
        # Do not pass values before this date
        fromdate=fromdate,
        # Do not pass values after this date
        todate=todate,
        reverse=False,
        dtformat=('%Y-%m-%d'),
        volume=6)
    
    init_close, fin_close = find_init_fin(datafile, fromdate, todate)
    data_output[datafile].append(fin_close/init_close - 1)
    data_output[datafile].append(init_close/fin_close - 1)
    
    return data

def run_model(data_output, datafile: str, data, model, param, simplename: str = "", count: int = 0):
    """
    Actual execution
    """
    # initialize driver & add strategy
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.Broker)
    cerebro.addstrategy(model, param)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    cerebro.broker.setcash(10000000)
    cerebro.run()
    data_output[datafile].append(cerebro.broker.getvalue()/10000000 - 1)
    if SAVE_PLOTS:
        # change backtrader's plot.py's show(self) into "pass"
        # so that no plots will be displayed
        img = cerebro.plot()[0][0]
        img.savefig(f"imgs2/{simplename}_{key_dict[count]}.png")


def run_experiments(data_output: dict, datafile: str, data, models: list, params: list, simplename: str = ""):
    """
    Runs executions with loops
    """
    simplename = datafile if simplename == "" else simplename
    count = 0
    for j, model in enumerate(models):
        for param in params[j]:
            run_model(data_output, datafile, data, model, param, simplename, count)
            count += 1

def save_result(data_output: list, params: list = [], header: list = []):
    """
    Saves result
    """
    header = ['name', 'release_date', 'result', 'stage', 'long', 'short', 'inverse 0.5', 'bollinger 0.5', 'bollinger 2.0', 'sma'] \
        if not header else header
    csv_write = open(f"output{'_'.join(params)}.csv", 'w')
    writer = csv.writer(csv_write)
    writer.writerow(header)
    for dt_output in data_output:
        writer.writerow(data_output[dt_output])
    csv_write.close()

if __name__ == '__main__':
    SAVE_PLOTS = True
    # setups
    data_output = {}
    datafiles = glob('./data/*_*_*_*_*_*.csv')
    
    meta_data, simple_names = regex_process(datafiles)
    models = [inverse_bollinger, bollinger, sma]
    key_dict = ["INV", "BOL05", "BOL20", "SMA"]
    duration = 14 # days, before & after
    params = [[{"period": duration//2, "inner_devfactor": 0.5, "order_ratio": sigma_to_frequency(0.5, 2*duration), "silence": True}],
              [{"period": duration//2, "inner_devfactor": 0.5, "order_ratio": sigma_to_frequency(0.5, 2*duration), "silence": True},
              {"period": duration//2, "inner_devfactor": 2.0, "order_ratio": sigma_to_frequency(2.0, 2*duration), "silence": True}],
              [{"period": duration//2, "order_ratio": 0.30, "silence": True}]]
    period = datetime.timedelta(days=int(duration/5*7))

    for i, datafile in enumerate(datafiles):
        print(simple_names[i], meta_data[i])
        data_output[datafile] = meta_data[i] # adds: name, release_date, result, stage
        # meta_data[i][1]: release date of trial
        data = stock_data_init(datafile, meta_data[i][1], period, data_output) # adds: long, short result
        run_experiments(data_output, datafile, data, models, params, simple_names[i])

    save_result(data_output)