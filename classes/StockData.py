"""Cleaned version of StockData.

This should be an application specific, smaller version of stock data.
"""
from collections import defaultdict
from collections import OrderedDict
import datetime
import math


class StockData:

  date_increment = None
  ticker = None
  name = None
  expense_ratio = None
  price_changes_by_increment = OrderedDict()

  def __init__(self, raw_stock_data, annual_expense_ratio, date_increment):
    if not date_increment in ('week', 'month', 'quarter', 'year'):
        raise ValueError('Unknown date increment %s.' % date_increment)

    self.date_increment = date_increment
    self.ticker = raw_stock_data.ticker
    self.name = raw_stock_data.name

    self._setExpenseRatio(annual_expense_ratio)

    self._setPriceData(raw_stock_data)

  def _setExpenseRatio(self, annual_expense_ratio):
    """Converts the expense ratio as needed."""
    if self.date_increment == 'week':
      self.expense_ratio = pow(1 - annual_expense_ratio, 1 / (365 / 7))
    if self.date_increment == 'month':
      self.expense_ratio = pow(1 - annual_expense_ratio, 1 / 12)
    elif self.date_increment == 'quarter':
      self.expense_ratio = pow(1 - annual_expense_ratio, 1 / 4)
    elif self.date_increment == 'year':
      self.expense_ratio = 1 - annual_expense_ratio

  def _setPriceData(self, raw_stock_data):
    """Converts raw price data to price_changes_by_date."""

    # Split prices by date increment.
    prices_and_dates_by_increment = defaultdict(list)

    for date_str, price in raw_stock_data.prices_by_date.items():
      date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

      if self.date_increment == 'week':
        epoch = datetime.datetime.utcfromtimestamp(0)
        days_since_epoch = (date - epoch).days
        # Epoch was a Thursday, so shift the days to get first day of each
        # week on Sunday.
        days_since_epoch -= 2
        increment = math.ceil(days_since_epoch / 7)
      if self.date_increment == 'month':
        increment = (date.year * 12) + date.month
      elif self.date_increment == 'quarter':
        increment = (date.year * 4) + math.ceil(date.month / 4)
      elif self.date_increment == 'year':
        increment = date.year

      prices_and_dates_by_increment[increment].append((date, price))

    # For each date increment, set date as end of increment, and price change as
    # last price in current increment over last price in previous increment.
    sorted_prices_and_dates_by_increment = sorted(
      prices_and_dates_by_increment.items())

    prev_data = None
    for data in sorted_prices_and_dates_by_increment:
      if not prev_data:
        prev_data = data
        continue

      max_price_this_increment = sorted(data[1], reverse=True)[0][1]
      max_price_prev_increment = sorted(prev_data[1], reverse=True)[0][1]
      price_change = (
        max_price_this_increment
          / max_price_prev_increment) * self.expense_ratio

      prev_data = data
      self.price_changes_by_increment[data[0]] = price_change
