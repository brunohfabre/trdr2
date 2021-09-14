def get_mg2_rate(candle):
  if candle['status'] == 'win' and candle['position'] == 'mg2':
    return True

  return False
