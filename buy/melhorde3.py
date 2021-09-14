import os, sys
from datetime import datetime
from time import time, sleep

from iqoptionapi.stable_api import IQ_Option

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from user import user

Iq = IQ_Option(user['username'], user['password'])
check, reason = Iq.connect()

if check:
  print('Successfully connected')

else:
  print('Connection error :/')

  sys.exit()

Iq.change_balance('PRACTICE')

balance = Iq.get_balance()
entry_value_base = round(balance * 0.01)
entry_value = entry_value_base

asset = input('Asset: ').upper()

print("Aguardando oportunidade de entrada")

def martingale():
  global entry_value
  global asset

  payout = round(int(Iq.get_digital_payout(asset)) / 100, 2)

  entry_value = (entry_value + (entry_value * payout)) / payout

while True:
  minutes = float(((datetime.now()).strftime('%M.%S'))[1:])

  if True if (minutes >= 3.58 and minutes <= 4) or (minutes >= 8.58 and minutes <= 9) else False:
    dir = False
    candles = Iq.get_candles(asset, 60, 8, time())

    candles[0] = 'g' if candles[0]['close'] > candles[0]['open'] else 'r' if candles[0]['close'] < candles[0]['open'] else 'd'
    candles[1] = 'g' if candles[1]['close'] > candles[1]['open'] else 'r' if candles[1]['close'] < candles[1]['open'] else 'd'
    candles[2] = 'g' if candles[2]['close'] > candles[2]['open'] else 'r' if candles[2]['close'] < candles[2]['open'] else 'd'
    
    candles[6] = 'g' if candles[6]['close'] > candles[6]['open'] else 'r' if candles[6]['close'] < candles[6]['open'] else 'd'
    candles[7] = 'g' if candles[7]['close'] > candles[7]['open'] else 'r' if candles[7]['close'] < candles[7]['open'] else 'd'

    colors = candles[0] + ' ' + candles[1] + ' ' + candles[2]
    result = f'{candles[6]} {candles[7]}'
	
    if colors.count('g') > colors.count('r') and colors.count('d') == 0 : dir = 'call'
    if colors.count('r') > colors.count('g') and colors.count('d') == 0 : dir = 'put'

    result = False if result.count('r' if dir == 'put' else 'g') else True

    print(colors)

    if dir and result:
      print('Direção:', dir)

      buy_status, id = Iq.buy_digital_spot_v2(asset, entry_value, dir, 1)

      if buy_status:
        while True:
          check_close, win_money= Iq.check_win_digital_v2(id)

          if check_close:
            if float(win_money) > 0:
              win_money=("%.2f" % (win_money))
              print("you win", win_money, "money")

              sys.exit()

            else:
              print("you loose\n")

              martingale()

              break
      
      else:
        print('Error entry')
    
    else:
      sleep(3)
      print(f'{candles[6]} {candles[7]}\n')
  
  sleep(0.5)