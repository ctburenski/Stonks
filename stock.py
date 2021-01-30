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
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={sym}&token={token}',
            headers={'Cache-Control': 'no-cache'})
    t = requests.get(f'https://finnhub.io/api/v1/search?q={sym}&token={token}',
            headers={'Cache-Control': 'no-cache'})

    for sym_result in t.json()['result']:
        if sym_result['displaySymbol'] == sym:
            return r.json()['c']
        else:
            raise NoValue

