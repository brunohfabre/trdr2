def get_win_rate(candle):
  if candle['status'] == 'win' and candle['position'] == 'init':
    return True

  return False
