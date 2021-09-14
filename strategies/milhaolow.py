from datetime import datetime

from helpers.get_win_rate import get_win_rate
from helpers.get_mg1_rate import get_mg1_rate
from helpers.get_mg2_rate import get_mg2_rate
from helpers.get_hit_rate import get_hit_rate

def milhaolow(asset, period):
  candles = []

  for i, candle in enumerate(asset['candles']):
    min = int(datetime.fromtimestamp(candle['from']).strftime('%M')[1:])

    if i > 4 and i < len(asset['candles']) - 3 and (min == 0 or min == 5):
      candles.append(candle)
  
  result = []

  for candle in candles:
    find_candle_index = asset['candles'].index(candle)

    analisys_candles = [
      asset['candles'][find_candle_index - 5],
      asset['candles'][find_candle_index - 4],
      asset['candles'][find_candle_index - 3],
      asset['candles'][find_candle_index - 2],
      asset['candles'][find_candle_index - 1]
    ]

    entry = ''

    colors = f"{analisys_candles[0]['color']} {analisys_candles[1]['color']} {analisys_candles[2]['color']}"

    if colors.count('doji') > 0:
      candle['status'] = 'doji'
      candle['position'] = 'init'

      result.append(candle)

    else:
      if colors.count('green') >= 3:
        entry = 'red'
      else:
        entry = 'green'

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
    "strategy": "milhaolow",
    "win": len(list(filter(get_win_rate, result))),
    "mg1": len(list(filter(get_mg1_rate, result))),
    "mg2": len(list(filter(get_mg2_rate, result))),
    "hit": len(list(filter(get_hit_rate, result))),
  }