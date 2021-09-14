def get_assets(Iq, type):
  assets = Iq.get_all_open_time()

  result = []

  for asset in assets[type]:
    if assets[type][asset]['open']:
      result.append(asset)

  return result