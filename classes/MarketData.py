"""Combination of multiple StockData objects into one.

StockData objects are filtered for several rules.
"""
import numpy as np


class MarketData:

  ticker_tuple = None
  date_tuple = None
  # Rows = Dates, Columns = Tickers
  return_matrix = None

  def __init__(self, stock_data_iterable, min_date, max_date):
    self.date_tuple = tuple(range(min_date, max_date + 1))

    ticker_list = []
    return_list = []
    for stock_data in stock_data_iterable:
      new_row = []
      for date in self.date_tuple:
        if date in stock_data.price_changes_by_increment:
          new_row.append(stock_data.price_changes_by_increment[date])

      # Skip tickers without all needed data.
      if len(new_row) < len(self.date_tuple):
        continue

      ticker_list.append(stock_data.ticker)
      return_list.append(new_row)

    self.ticker_tuple = tuple(ticker_list)
    self.return_matrix = np.array(return_list, dtype=np.float64).T

  def getSlice(self, min_date, max_date):
    """Get a slice of data from within the set."""
    if max_date > max(self.date_tuple) or min_date < min(self.date_tuple):
      raise ValueError(
        'Min and Max dates must be within %d-%d' % (
          max(self.date_tuple), min(self.date_tuple)))

    min_offset = min_date - min(self.date_tuple)
    max_offset = max_date - min(self.date_tuple) + 1
    new_array = self.return_matrix[min_offset:max_offset]
    return new_array
