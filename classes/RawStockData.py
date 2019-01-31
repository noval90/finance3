"""Class to represent raw data about a given stock.

The goal of this class is to be extremely small and simple, so that it is
portable between implementations.
"""

class RawStockData:

  def __init__(self, ticker, name, prices_by_date):
    # Ticker should be a normal stock ticker (e.g., MSFT).
    self.ticker = ticker
    # Name should be the common name of the company (e.g., Microsoft, Inc.)
    self.name = name
    # Prices by date should be a map of prices to date strings.
    # (e.g., '2007-01-01': 100.12 
    self.prices_by_date = prices_by_date

