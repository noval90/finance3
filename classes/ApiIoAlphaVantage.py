"""Handles retrieving stock data from an API."""
from .ApiIo import ApiIo
import datetime
import requests
import time


class ApiIoAlphaVantage(ApiIo):

  api_key = None

  SEARCH_REQUEST_BASE = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=%s&apikey=%s'
  PRICE_REQUEST_BASE = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s'

  def __init__(self, api_key):
    self.api_key = api_key

  def _callApi(self, request, required_result_key):
    """Try the given request with retries."""
    aggregated_results = {}
    for _ in range(120):
      time.sleep(1)

      raw_result = requests.get(request)

      # Retry w/o error if server is overloaded.
      if raw_result.status_code == 503:
        continue

      # Error on other status codes.
      if raw_result.status_code != 200:
        raise IOError('Received code %s for request\n%s\nGot data:\n%s' % (
          raw_result.status_code, request, raw_result))

      try:
        json_result = raw_result.json()
      except Exception as e:
        print(request)
        print(raw_result)
        raise e

      if 'Error Message' in json_result:
        raise IOError('Received error\n%s\nfor request\n%s' % (json_result, request))

      if required_result_key not in json_result:
        aggregated_results.update(json_result)
        continue

      return json_result

    print(aggregated_results)
    raise IOError('Too many attempts for request %s.' % request)

  def _getPriceData(self, ticker):
    """Get's price data for the ticker."""
    request = self.PRICE_REQUEST_BASE % (ticker, self.api_key)
    result = self._callApi(request, 'Time Series (Daily)')

    price_data = {}
    for date_str, data in result['Time Series (Daily)'].items():
      price_float = float(data['5. adjusted close'])
      price_data[date_str] = price_float

    return price_data


  def _getName(self, ticker):
    """Get's the name of the ticker's stock."""
    request = self.SEARCH_REQUEST_BASE % (ticker, self.api_key)
    result = self._callApi(request, 'bestMatches')

    for match in result['bestMatches']:
      if match['1. symbol'] == ticker:
        return match['2. name']

    raise IOError('Countn\'t find ticker %s' % ticker)

  def getAll(self, ticker):
    """Returns a RawStockData object about the given ticker."""
    name = self._getName(ticker)
    prices_by_date = self._getPriceData(ticker)

    return RawStockData(ticker, name, prices_by_date)

