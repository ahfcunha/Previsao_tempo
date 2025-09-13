import requests
import json

cidade = input('De qual cidade você deseja saber o clima? ')

URL_localizacao = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=5"

try:
  resp1 = requests.get(URL_localizacao)

  cidades_encontradas = []
  if resp1.status_code == 200:
    dados_loc = resp1.json()

    for i in dados_loc['results']:
      cidades_encontradas.append({"nome": i["name"], "latitude": i["latitude"], "longitude": i["longitude"], "estado": i['admin1'], "país": i["country"]})
    for j, k in enumerate(cidades_encontradas):
      print(f"{j + 1}) {k['nome']}, {k['estado']}, {k['país']}")

    indice_cidade = int(input("A cidade que você deseja é uma dessas? "))

  else:
    print(f'Erro {resp1.status_code} ao localizar dados')

except Exception as e:
  print(f'Ocorreu um erro {e}')

latitude = cidades_encontradas[indice_cidade - 1]['latitude']
longitude = cidades_encontradas[indice_cidade - 1]['longitude']

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