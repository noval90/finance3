"""Tests for the MaketData Class."""
from .MarketData import MarketData
from .RawStockData import RawStockData
from .StockData import StockData
import unittest


class TestInit(unittest.TestCase):

  def test_normal(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01,
      3: 1.02,
      4: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)

    self.assertTupleEqual(market_data.ticker_tuple, ('test',))
    self.assertTupleEqual(market_data.date_tuple, (1, 2, 3))
    self.assertTupleEqual(tuple(market_data.return_matrix[0]), (1.02,))
    self.assertTupleEqual(tuple(market_data.return_matrix[1]), (1.01,))
    self.assertTupleEqual(tuple(market_data.return_matrix[2]), (1.02,))
    self.assertEqual(len(market_data.return_matrix), 3)

  def test_min_exclusion(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      2: 1.01,
      3: 1.02,
      4: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)

    self.assertTupleEqual(market_data.ticker_tuple, tuple())
    self.assertTupleEqual(market_data.date_tuple, (1, 2, 3))
    self.assertEqual(len(market_data.return_matrix), 0)

  def test_max_exclusion(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)

    self.assertTupleEqual(market_data.ticker_tuple, tuple())
    self.assertTupleEqual(market_data.date_tuple, (1, 2, 3))
    self.assertEqual(len(market_data.return_matrix), 0)

  def test_mid_exclusion(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      3: 1.02,
      4: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)

    self.assertTupleEqual(market_data.ticker_tuple, tuple())
    self.assertTupleEqual(market_data.date_tuple, (1, 2, 3))
    self.assertEqual(len(market_data.return_matrix), 0)

class TestSlice(unittest.TestCase):

  def test_too_low_slice(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)
    
    with self.assertRaises(ValueError):
      market_data.getSlice(min_date=0)

  def test_too_high_slice(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01}
    market_data = MarketData([stock_data], min_date, max_date)
    with self.assertRaises(ValueError):
      market_data.getSlice(max_date=4)

  def test_good_slice(self):
    min_date = 1
    max_date = 3
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data = StockData(raw_stock_data, 0, 'week')
    stock_data.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01,
      3: 1.02}
    market_data = MarketData([stock_data], min_date, max_date)
    
    market_slice = market_data.getSlice(min_date=1, max_date=2)
    self.assertEqual(len(market_slice), 2)
    self.assertEqual(market_slice[0], [1.02])
    self.assertEqual(market_slice[1], [1.01])

  def test_ticker_slice(self):
    raw_stock_data = RawStockData('test', 'test', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 101.00})
    stock_data_1 = StockData(raw_stock_data, 0, 'week')
    stock_data_1.price_changes_by_increment = {
      0: 1.01,
      1: 1.02,
      2: 1.01,
      3: 1.02}
    raw_stock_data = RawStockData('test1', 'test1', {
                    '2007-01-01': 100.00,
                    '2007-01-08': 102.00})
    stock_data_2 = StockData(raw_stock_data, 0, 'week')
    stock_data_2.price_changes_by_increment = {
      0: 1.02,
      1: 1.03,
      2: 1.04,
      3: 1.05}
    market_data = MarketData([stock_data_1, stock_data_2], 1, 3)

    market_slice = market_data.getSlice(tickers=('test1',))
    self.assertEqual(market_slice[0][0], 1.03)

