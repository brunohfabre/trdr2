import sys
from datetime import datetime
from time import time, sleep

def milhao(Iq, asset):
  balance = Iq.get_balance()
  entry_value_base = round(balance * 0.01)
  entry_value = entry_value_base

  print(f"Aguardando oportunidade de entrada. {asset} Milhão")

  def martingale(entry_value):
    payout = round(int(Iq.get_digital_payout(asset)) / 100, 2)

    entry_value = (entry_value + (entry_value * payout)) / payout

  while True:
    minutes = float(((datetime.now()).strftime('%M.%S'))[1:])

    if True if (minutes >= 1.58 and minutes <= 2) or (minutes >= 6.58 and minutes <= 7) else False:
      dir = False
      candles = Iq.get_candles(asset, 60, 7, time())

      candles[0] = 'g' if candles[0]['close'] > candles[0]['open'] else 'r' if candles[0]['close'] < candles[0]['open'] else 'd'
      candles[1] = 'g' if candles[1]['close'] > candles[1]['open'] else 'r' if candles[1]['close'] < candles[1]['open'] else 'd'
      candles[2] = 'g' if candles[2]['close'] > candles[2]['open'] else 'r' if candles[2]['close'] < candles[2]['open'] else 'd'
      candles[3] = 'g' if candles[3]['close'] > candles[3]['open'] else 'r' if candles[3]['close'] < candles[3]['open'] else 'd'
      candles[4] = 'g' if candles[4]['close'] > candles[4]['open'] else 'r' if candles[4]['close'] < candles[4]['open'] else 'd'

      candles[5] = 'g' if candles[5]['close'] > candles[5]['open'] else 'r' if candles[5]['close'] < candles[5]['open'] else 'd'
      candles[6] = 'g' if candles[6]['close'] > candles[6]['open'] else 'r' if candles[6]['close'] < candles[6]['open'] else 'd'

      colors = candles[0] + ' ' + candles[1] + ' ' + candles[2]
      result = f'{candles[5]} {candles[6]}'
    
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

                martingale(entry_value)

                break
        
        else:
          print('Error entry')
      
      else:
        sleep(3)
        print(f'{candles[5]} {candles[6]}\n')
    
    sleep(0.5)