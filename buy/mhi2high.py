from datetime import datetime
from time import time, sleep

from helpers.martingale import martingale

def mhi2high(Iq, asset, initial_entry, entry):
  balance = Iq.get_balance()
  entry_value_base = round(balance * (entry / 100))
  entry_value = entry_value_base
  loss = 0
  payout = round(int(Iq.get_digital_payout(asset)) / 100, 2)
  martingale_count = 3

  if initial_entry != 0:
    entry_value = martingale(Iq, asset, initial_entry)

  print(f"Aguardando oportunidade de entrada. {asset} MHI 2 maioria")

  while True:
    minutes = float(((datetime.now()).strftime('%M.%S'))[1:])

    if True if (minutes >= 0.59 and minutes <= 1) or (minutes >= 5.59 and minutes <= 6) else False:
      dir = False
      candles = Iq.get_candles(asset, 60, 4, time())

      candles[0] = 'g' if candles[0]['close'] > candles[0]['open'] else 'r' if candles[0]['close'] < candles[0]['open'] else 'd'
      candles[1] = 'g' if candles[1]['close'] > candles[1]['open'] else 'r' if candles[1]['close'] < candles[1]['open'] else 'd'
      candles[2] = 'g' if candles[2]['close'] > candles[2]['open'] else 'r' if candles[2]['close'] < candles[2]['open'] else 'd'

      colors = candles[0] + ' ' + candles[1] + ' ' + candles[2]
    
      if colors.count('g') > colors.count('r') and colors.count('d') == 0 : dir = 'call'
      if colors.count('r') > colors.count('g') and colors.count('d') == 0 : dir = 'put'

      print(colors)

      if dir:
        print('Direção:', dir)

        for i in range(martingale_count):
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
                  entry_value = martingale(entry_value, payout)

                  break
          
          else:
            print('Error entry')

            return ('loss', loss)
      
      else:
        sleep(3)
        print(f'{candles[4]} {candles[5]}\n')
    
    sleep(0.2)