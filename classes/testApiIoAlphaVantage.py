"""Tests for the AlphaVantage API wrapper."""

from .ApiIoAlphaVantage import ApiIoAlphaVantage
import unittest 


class TestGetName(unittest.TestCase):

  def test_generalTicker(self):
    actual = ApiIoAlphaVantage('demo')._getName('BA')
    expected = 'The Boeing Company'

    self.assertEqual(actual, expected)

  def test_badTicker(self):
    with self.assertRaises(IOError):
      ApiIoAlphaVantage('demo')._getName('Micro')


class TestGetPriceData(unittest.TestCase):

  def test_generalTicker(self):
    actual = ApiIoAlphaVantage('demo')._getPriceData('MSFT')

    self.assertGreater(len(actual), 0)
    for date_str, price in actual.items():
      self.assertRegex(date_str, '[0-9]{4}-[0-9]{2}-[0-9]{2}')
      self.assertIsInstance(price, float)

