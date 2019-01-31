"""Tests for the StockData Class."""
from .RawStockData import RawStockData
from .StockData import StockData
import unittest


class TestInit(unittest.TestCase):

  def test_bad_increment(self):
    raw_stock_data = RawStockData('test', 'test', {
        '2007-01-01': 100.00})
    with self.assertRaises(ValueError):
      stock_data = StockData(raw_stock_data, 0.0, 'bad_increment')

  def test_direct_assignment(self):
    raw_stock_data = RawStockData('test_ticker', 'test_name', {
        '2007-01-01': 100.00,
        '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0.0, 'week')

    self.assertEqual(stock_data.date_increment, 'week')
    self.assertEqual(stock_data.ticker, 'test_ticker')
    self.assertEqual(stock_data.name, 'test_name')

  def test_expense_ratio(self):
    raw_stock_data = RawStockData('test_ticker', 'test_name', {
        '2007-01-01': 100.00,
        '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0.01, 'week')
    
    self.assertAlmostEqual(stock_data.expense_ratio, 0.9998073)

  def test_price_data(self):
    raw_stock_data = RawStockData('test_ticker', 'test_name', {
        '2007-01-01': 100.00,
        '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0.0, 'week')

    self.assertListEqual(
      list(stock_data.price_changes_by_increment.keys()), [1932])
    self.assertListEqual(
      list(stock_data.price_changes_by_increment.values()), [1.01])

