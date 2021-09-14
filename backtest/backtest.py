from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import sys, json
from user import user

Iq = IQ_Option(user['username'], user['password'])
Iq.connect()

Iq.change_balance('PRACTICE')

if Iq.check_connect():
  print('Conectado com sucesso.')
else:
  print('Erro ao conectar.')

  input('\n\nAperte enter para sair.')
  sys.exit()

file = open('sinais.json', 'r').read()
days = json.loads(file)

def getCandleColor(candle):
  if candle['close'] > candle['open']:
    return 'green'
  
  if candle['close'] < candle['open']:
    return 'red'

  return 'doji'

response = []

for day in days:
  dayResponse = {
    'date': day['date'],
    'operations': []
  }

  for operation in day['operations']:
    data = operation.split(';')

    date = datetime.strptime(day['date'] + ' ' + data[0] + ':00', '%Y-%m-%d %H:%M:%S') + timedelta(minutes = 10)
    candles = Iq.get_candles(data[1], 60 * int(data[3]), 3, date.timestamp())

    entry = 'green' if data[2] == 'CALL' else 'red'
    result = 'doji'

    if(getCandleColor(candles[0]) == entry):
      result = 'win'

    elif(getCandleColor(candles[1]) == entry):
      result = 'mg1'

    elif(getCandleColor(candles[2]) == entry):
      result = 'mg2'
    
    else:
      result = 'loss'

    dayResponse['operations'].append(operation + ';' + result)
  
  response.append(dayResponse)

resultFile = open('resultado.json', 'w')
json.dump(response, resultFile)