def get_mg1_rate(candle):
  if candle['status'] == 'win' and candle['position'] == 'mg1':
    return True

  return False
