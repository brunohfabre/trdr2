import sys
from iqoptionapi.stable_api import IQ_Option

from user import user

from get_assets import get_assets
from get_candles import get_candles
from process_strategies import process_strategies

Iq = IQ_Option(user['username'], user['password'])
check, reason = Iq.connect()

if check:
  print('Successfully connected')

else:
  print('Connection error :/')

  sys.exit()

period = 1

assets = get_assets(Iq, 'digital')

candles = get_candles(Iq, assets, period)

strategies = process_strategies(candles, period)

strategies.reverse()

print(strategies[0])