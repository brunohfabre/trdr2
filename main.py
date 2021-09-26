import sys, configparser
from iqoptionapi.stable_api import IQ_Option

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

settings = configparser.RawConfigParser()
settings.read('settings.txt')

Iq = IQ_Option(settings.get('ACCOUNT', 'user'), settings.get('ACCOUNT', 'password'))
check, reason = Iq.connect()

if check:
  print('Successfully connected\n')

else:
  print('Connection error :/')

  sys.exit()


balance = Iq.get_balance()
profit = 0
stop = int(settings.get('OPERATION', 'stop'))
gain = round(balance * (stop / 100))
period = int(settings.get('OPERATION', 'catalog'))
loss = 0
entry = int(settings.get('OPERATION', 'entry'))
account_type = settings.get('ACCOUNT', 'type')

strategies_to_execute = {}

Iq.change_balance(account_type)

print(f'account type: {account_type}')
print(f'balance: {balance}')
print(f'stop win: {stop}%, {gain}')
print(f'catalog period: {period}h')
print(f'entry value: {entry}%, {round(balance * (entry / 100), 2)}\n')

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
  global entry
  global strategies_to_execute

  assets = get_assets(Iq, 'digital')

  for asset in assets:
    strategies_to_execute[asset] = {
      'mhi': 2,
      'mhihigh': 2,
      'mhi2': 2,
      'mhi2high': 2,
      'mhi3': 2,
      'mhi3high': 2,
      'milhao': 2,
      'milhaolow': 2,
      'torresgemeas': 2,
      'melhorde3': 2,
      'padrao23': 2,
      'tresmosqueteiros': 2,
    }

  candles = get_candles(Iq, assets, period)

  strategies = process_strategies(candles, period, strategies_to_execute)

  strategies.reverse()

  strategy = strategies[0]

  print(strategy)

  buy = buys[strategy['strategy']]

  result, money = buy(Iq, strategy['asset'], loss, entry)

  if result == 'win':
    profit = profit + money
    loss = 0
    strategies_to_execute[strategy['asset']][strategy['strategy']] -= 1

  else:
    loss = money
    strategies_to_execute[strategy['asset']][strategy['strategy']] = 0

  print(profit, loss)

  stop_win()
  return

while True:
  run()
