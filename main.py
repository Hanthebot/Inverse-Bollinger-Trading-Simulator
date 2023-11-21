import datetime

import backtrader as bt

from strategy import inverse_bollinger, bollinger, hodl_long, hodl_short

if __name__ == '__main__':
    # initialize driver & add strategy
    cerebro = bt.Cerebro()
    custom_params = {} #{"inner_devfactor": 2.0}
    cerebro.addstrategy(bollinger, custom_params)
    
    datapath = './data/MSFT_2020-01-01_2023-06-30.csv'
    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2023, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2023, 6, 30),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.broker.setcash(10000000)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()