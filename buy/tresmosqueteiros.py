from datetime import datetime
from time import time, sleep

from helpers.martingale import martingale

def tresmosqueteiros(Iq, asset, initial_entry):
  balance = Iq.get_balance()
  entry_value_base = round(balance * 0.01)
  entry_value = entry_value_base
  loss = 0

  if initial_entry != 0:
    entry_value = martingale(Iq, asset, initial_entry)

  print(f"Aguardando oportunidade de entrada. {asset} Tres mosqueteiros")

  while True:
    minutes = float(((datetime.now()).strftime('%M.%S'))[1:])

    if True if (minutes >= 4.59 and minutes <= 5) or minutes >= 9.59 else False:
      dir = False
      candles = Iq.get_candles(asset, 60, 3, time())

      candles[0] = 'g' if candles[0]['close'] > candles[0]['open'] else 'r' if candles[0]['close'] < candles[0]['open'] else 'd'
      candles[1] = 'g' if candles[1]['close'] > candles[1]['open'] else 'r' if candles[1]['close'] < candles[1]['open'] else 'd'
      candles[2] = 'g' if candles[2]['close'] > candles[2]['open'] else 'r' if candles[2]['close'] < candles[2]['open'] else 'd'

      result = f'{candles[1]} {candles[2]}'
    
      if candles[0] == 'g' : dir = 'call'
      if candles[0] == 'r' : dir = 'put'

      result = False if result.count('r' if dir == 'put' else 'g') else True

      print(candles[0])

      if dir and result:
        print('Direção:', dir)

        buy_status, id = Iq.buy_digital_spot_v2(asset, entry_value, dir, 1)

        if buy_status:
          while True:
            check_close, win_money = Iq.check_win_digital_v2(id)

            if check_close:
              if float(win_money) > 0:
                win_money = round(float(win_money), 2)
                value = win_money - loss
                
                print("you win", value, "money")

                return ('win', value)

              else:
                print("you loose\n")

                loss += entry_value
                entry_value = martingale(Iq, asset, entry_value)

                break
        
        else:
          print('Error entry')

          return ('loss', loss)
      
      else:
        sleep(3)
        print(f'{candles[1]} {candles[2]}\n')
    
    sleep(0.2)