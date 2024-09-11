# region imports
from AlgorithmImports import *
# endregion

class Tutorial1(QCAlgorithm):

    def initialize(self):
        # Locally Lean installs free sample data, to download more data please visit https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 3, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.spy = self.AddEquity("SPY", Resolution.DAILY)
        self.spy.SetDataNormalizationMode(DataNormalizationMode.ADJUSTED)

        self.spy_symbol = self.spy.Symbol
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.CASH)

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
        price = data[self.spy_symbol].Close
        if self.Portfolio.Invested:
            if self.time >= self.nextEntryTime:
                self.SetHoldings(self.spy_symbol, 1)
                self.Debug("Purchased Stock @ " + str(price))
                self.nextEntryTime = self.time + self.period
                self.entryPrice = price
        elif price > self.entryPrice*1.1 or price < self.entryPrice*0.9:
            self.SetHoldings(self.spy_symbol, 0)
            self.Debug("Sold Stock @ " + str(price))
            self.nextEntryTime = self.time + self.period

