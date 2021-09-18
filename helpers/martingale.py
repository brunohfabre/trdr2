def martingale(Iq, asset, value):
  payout = round(int(Iq.get_digital_payout(asset)) / 100, 2)

  new_value = (value + (value * payout)) / payout

  return new_value