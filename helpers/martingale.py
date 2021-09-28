def martingale(value, payout):
  new_value = (value + (value * payout)) / payout

  return new_value