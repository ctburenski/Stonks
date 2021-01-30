import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.getenv('STOCK_TOKEN')


class NoValue(Exception):
  pass


def price(sym):
  sym = sym.upper()
  find_stock = f'https://finnhub.io/api/v1/search?q={sym}&token={token}'
  print(find_stock)
  t = requests.get(find_stock)

  get_stock = f'https://finnhub.io/api/v1/quote?symbol={sym}&token={token}'
  print(get_stock)
  r = requests.get(get_stock)

  for sym_result in t.json()['result']:
    print(sym_result['symbol'], sym)
    if sym_result['symbol'] == sym:
      return r.json()['c']
  print(t.json()['result'])
  raise NoValue
