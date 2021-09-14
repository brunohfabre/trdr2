from datetime import datetime

from helpers.get_win_rate import get_win_rate
from helpers.get_mg1_rate import get_mg1_rate
from helpers.get_mg2_rate import get_mg2_rate
from helpers.get_hit_rate import get_hit_rate

def padrao23(asset, period):
  candles = []

  for i, candle in enumerate(asset['candles']):
    min = int(datetime.fromtimestamp(candle['from']).strftime('%M')[1:])

    if i > 4 and i < len(asset['candles']) - 3 and (min == 1 or min == 6):
      candles.append(candle)
  
  result = []

  for candle in candles:
    find_candle_index = asset['candles'].index(candle)

    analisys_candle = asset['candles'][find_candle_index - 1]

    entry = analisys_candle['color']

    if entry == 'doji':
      candle['status'] = 'doji'
      candle['position'] = 'init'

      result.append(candle)

    else:
      if candle['color'] == entry:
        candle['status'] = 'win'
        candle['position'] = 'init'

        result.append(candle)
      
      elif asset['candles'][find_candle_index + 1]['color'] == entry:
        candle['status'] = 'win'
        candle['position'] = 'mg1'

        result.append(candle)

      elif asset['candles'][find_candle_index + 2]['color'] == entry:
        candle['status'] = 'win'
        candle['position'] = 'mg2'

        result.append(candle)

      else:
        candle['status'] = 'loss'
        candle['position'] = 'init'

        result.append(candle)

  result = result[len(result) - (period * 12):]

  return {
    "asset": asset['name'],
    "strategy": "padrao23",
    "win": len(list(filter(get_win_rate, result))),
    "mg1": len(list(filter(get_mg1_rate, result))),
    "mg2": len(list(filter(get_mg2_rate, result))),
    "hit": len(list(filter(get_hit_rate, result))),
  }