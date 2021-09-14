from datetime import datetime

def get_asset_candles(Iq, asset, last_period):
  time = datetime.now()
  
  hour = time.hour
  minutes = ((time.minute // 5 + 1) * 5) - 6

  current_time = datetime.now().replace(hour = hour - 1 if minutes < 4 else hour, minute = 59 if minutes < 4 else minutes, second = 0, microsecond = 0)

  candles_count = int((60 * last_period) + 10)

  candles = Iq.get_candles(asset, 60, candles_count, current_time.timestamp())

  result = []

  for candle in candles:
    candle['color'] = 'green' if candle['close'] > candle['open'] else 'red' if candle['close'] < candle['open'] else 'doji'

    result.append(candle)

  return {
    "name": asset,
    "candles": result
  }

result = []

def get_candles(Iq, assets, period):
  for asset in assets:
    result.append(get_asset_candles(Iq, asset, period))

  return result