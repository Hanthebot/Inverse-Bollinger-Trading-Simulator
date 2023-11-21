import backtrader as bt

class strategy_basic(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Margin]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f, %.2f' % (order.executed.price, order.executed.size))
            elif order.issell():
                self.log('SELL EXECUTED, %.2f, %.2f' % (order.executed.price, order.executed.size))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Rejected]:
            self.log('Order Canceled/Rejected')

        # Write down: no pending order
        self.order = None
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

class inverse_bollinger(strategy_basic):
    params = (
        ("period", 20),
        ("inner_devfactor", 0.5),
        ("outer_devfactor", 2.0),
        ("debug", False),
        ("order_size", 25),
        ("hodl_period", 10)
    )
    def __init__(self, params = None):
        # ref: https://stackoverflow.com/questions/72273407/can-you-add-parameters-to-backtrader-strategy
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        # self.datas: feed to the strategy
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        self.order_ratio = 0.10 # in percentage of total portfolio value
        self.boll_in = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.inner_devfactor, plot=True)
        # for view purpose only
        self.boll_out = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.outer_devfactor, plot=True)
        below_inbot = bt.indicators.CrossDown(self.data.close, self.boll_in.lines.bot)
        over_intop = bt.indicators.CrossOver(self.data.close, self.boll_in.lines.top)
        self.buy_signal = over_intop
        self.sell_signal = below_inbot

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        if self.order: # there is an open order
            return
        # Check if we are in the market
        #if not self.position.size: # not in position! can buy!
        if self.buy_signal:
            # Keep track of the created order to avoid a 2nd order
            price = self.boll_in.lines.top[0]
            # order smaller between: all cash available and a portion of total portfolio value
            cash_size = int(self.broker.getcash() / price) 
            portion_portforlio = int(self.broker.getvalue() * self.order_ratio / price)
            size = min(cash_size, portion_portforlio)
            self.log('BUY CREATE, %.2f, %d' % (price, size))
            if size != 0:
                self.order = self.buy(price = price, size = size)

        elif self.sell_signal:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            # self.log('SELL CREATE, %.2f' % self.dataclose[0])
            price = self.boll_in.lines.bot[0]
            #size = int(self.broker.getcash() / price)
            # Keep track of the created order to avoid a 2nd order
            # order smaller between: all position available and a portion of total portfolio value
            pos_size = self.position.size
            portion_portforlio = int(self.broker.getvalue() * self.order_ratio / price)
            size = min(pos_size, portion_portforlio)
            self.log('SELL CREATE, %.2f, %d' % (price, size))
            if size != 0:
                self.order = self.sell(price = price, size = size)

class bollinger(strategy_basic):
    params = (
        ("period", 20),
        ("inner_devfactor", 0.5),
        ("outer_devfactor", 2.0),
        ("debug", False),
        ("order_size", 25),
        ("hodl_period", 10)
    )
    def __init__(self, params = None):
        # ref: https://stackoverflow.com/questions/72273407/can-you-add-parameters-to-backtrader-strategy
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        # self.datas: feed to the strategy
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        self.order_ratio = 0.10 # in percentage of total portfolio value
        self.boll_in = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.inner_devfactor, plot=True)
        # for view purpose only
        self.boll_out = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.outer_devfactor, plot=True)
        below_inbot = bt.indicators.CrossDown(self.data.close, self.boll_in.lines.bot)
        over_intop = bt.indicators.CrossOver(self.data.close, self.boll_in.lines.top)
        self.sell_signal = over_intop
        self.buy_signal = below_inbot

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        if self.order: # there is an open order
            return
        # Check if we are in the market
        #if not self.position.size: # not in position! can buy!
        if self.buy_signal:
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            price = self.boll_in.lines.bot[0]
            # order smaller between: all cash available and a portion of total portfolio value
            cash_size = int(self.broker.getcash() / price) 
            portion_portforlio = int(self.broker.getvalue() * self.order_ratio / price)
            size = min(cash_size, portion_portforlio)
            if size != 0:
                self.order = self.buy(price = price, size = size)

        elif self.sell_signal:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            price = self.boll_in.lines.top[0]
            #size = int(self.broker.getcash() / price)
            # Keep track of the created order to avoid a 2nd order
            # order smaller between: all position available and a portion of total portfolio value
            pos_size = self.position.size
            portion_portforlio = int(self.broker.getvalue() * self.order_ratio / price)
            size = min(pos_size, portion_portforlio)
            if size != 0:
                self.order = self.sell(price = price, size = size)

class hodl_long(strategy_basic):
    def __init__(self, params = None):
        # ref: https://stackoverflow.com/questions/72273407/can-you-add-parameters-to-backtrader-strategy
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        # self.datas: feed to the strategy
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
    
    def nextstart(self):
        # Buy all the available cash
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)

class hodl_short(strategy_basic):
    def __init__(self, params = None):
        # ref: https://stackoverflow.com/questions/72273407/can-you-add-parameters-to-backtrader-strategy
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        # self.datas: feed to the strategy
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        self.hodl_executed = False
    
    def nextstart(self):
        # Buy all the available cash
        size = int(self.broker.getvalue() / self.data)
        self.sell(size=size)

# direct reference: https://www.backtrader.com/docu/quickstart/quickstart/#google_vignette