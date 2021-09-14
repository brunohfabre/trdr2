def get_hit_rate(candle):
  if candle['status'] == 'loss':
    return True

  return False
