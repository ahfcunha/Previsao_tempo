import requests
import json

latitude = -23.5489
longitude = -46.6388

URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation_probability&hourly=temperature_2m,precipitation_probability,wind_speed_10m"

try:
  resp2 = requests.get(URL)

  if resp2.status_code == 200:
    dados_clima = resp2.json()

    temperatura_atual = dados_clima['current']['temperature_2m']
    chuva_agr = dados_clima['current']['precipitation_probability']

    print('***PREVISÃO DO TEMPO PARA A SUA LOCALIDADE***')
    print(f'TEMPERATURA: {temperatura_atual}°C')
    print(f'PROBABILIDADE DE CHUVA: {chuva_agr}%')
  else:
    print(f'Erro {resp2.status_code} ao localizar dados')

except Exception as ex:
  print(f'Ocorreu um erro {ex}')