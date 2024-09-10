# region imports
from AlgorithmImports import *
# endregion

class Tutorial1(QCAlgorithm):

    def initialize(self):
        # Locally Lean installs free sample data, to download more data please visit https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data
        self.set_start_date(2013, 10, 7)  # Set Start Date
        self.set_end_date(2013, 10, 11)  # Set End Date
        self.set_cash(100000)  # Set Strategy Cash
        self.spy = self.add_equity("SPY", Resolution.DAILY)
        self.spy.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)

        self.spy_symbol = self.spy.symbol
        self.set_benchmark("SPY")
        self.set_brokerage_model(BrokerageModel.InteractiveBrokersBrokerage,AccountType.CASH)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.time
        



    def on_data(self, data: Slice):
        """on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        if not self.spy_symbol in data:
            return
        price = data[self.spy_symbol].close
        if self.Portfolio.invested:
            if self.time >= self.nextEntryTime:
                self.set_holdings(self.spy_symbol, 1)
                self.debug("Purchased Stock @ " + str(price))
                self.nextEntryTime = self.time + self.period
                self.entryPrice = price
        elif price > self.entryPrice*1.1 or price < self.entryPrice*0.9:
            self.set_holdings(self.spy_symbol, 0)
            self.debug("Sold Stock @ " + str(price))
            self.nextEntryTime = self.time + self.period

