import sys
from iqoptionapi.stable_api import IQ_Option

from user import user

from get_assets import get_assets
from get_candles import get_candles
from process_strategies import process_strategies

from buy.melhorde3 import melhorde3
from buy.mhi import mhi
from buy.mhi2 import mhi2
from buy.mhi2high import mhi2high
from buy.mhi3 import mhi3
from buy.mhi3high import mhi3high
from buy.mhihigh import mhihigh
from buy.milhao import milhao
from buy.milhaolow import milhaolow
from buy.padrao23 import padrao23
from buy.torresgemeas import torresgemeas
from buy.tresmosqueteiros import tresmosqueteiros

buys = {
  'melhorde3': melhorde3,
  'mhi': mhi,
  'mhi2': mhi2,
  'mhi2high': mhi2high,
  'mhi3': mhi3,
  'mhi3high': mhi3high,
  'mhihigh': mhihigh,
  'milhao': milhao,
  'milhaolow': milhaolow,
  'padrao23': padrao23,
  'torresgemeas': torresgemeas,
  'tresmosqueteiros': tresmosqueteiros,
}

Iq = IQ_Option(user['username'], user['password'])
check, reason = Iq.connect()

if check:
  print('Successfully connected')

else:
  print('Connection error :/')

  sys.exit()

Iq.change_balance('PRACTICE')

profit = 0
gain = round(Iq.get_balance() * 0.05)
period = 2
loss = 0

def stop_win():
  global profit
  global gain

  if(profit >= gain):
    print('Stop Win Batido!')

    sys.exit()

def run():
  global profit
  global gain
  global period
  global loss

  print(profit, loss)
  assets = get_assets(Iq, 'digital')

  candles = get_candles(Iq, assets, period)

  strategies = process_strategies(candles, period)

  strategies.reverse()

  strategy = strategies[0]
  print(strategy)

  buy = buys[strategy['strategy']]

  result, money = buy(Iq, strategy['asset'], loss)

  if result == 'win':
    profit = profit + money
    loss = 0

  else:
    loss = money

  stop_win()

while True:
  run()
