from strategies.mhi import mhi
from strategies.mhihigh import mhihigh
from strategies.mhi2 import mhi2
from strategies.mhi2high import mhi2high
from strategies.mhi3 import mhi3
from strategies.mhi3high import mhi3high
from strategies.milhao import milhao
from strategies.milhaolow import milhaolow
from strategies.torresgemeas import torresgemeas
from strategies.melhorde3 import melhorde3
from strategies.padrao23 import padrao23
from strategies.tresmosqueteiros import tresmosqueteiros

strategies = [
  mhi,
  mhihigh,
  mhi2,
  mhi2high,
  mhi3,
  mhi3high,
  milhao,
  milhaolow,
  torresgemeas,
  melhorde3,
  padrao23,
  tresmosqueteiros,
]

def process_strategies(assets, period):
  result = []

  for asset in assets:
    for strategy in strategies:
      response = strategy(asset, period)

      if response['hit'] == 0:
        result.append(response)

  result = sorted(result, key=lambda k: k['mg2'])

  return result