# Responsável por fazer requisições HTTP, ou seja, se comunicar com os servidores na internet
import requests
# Responsável por fazer a tradução entre uma string de texto em formato JSON e um objeto python
import json
from datetime import datetime



def buscar_cidades():

  cidade = input('De qual cidade você deseja saber o clima? \n')
  # URL base da API que retorna algumas informações sobre a cidade buscada
  URL_LOCALIZACAO = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=5"

  try:
    resp1 = requests.get(URL_LOCALIZACAO)

    cidades_encontradas = []
    print(' ')
    if resp1.status_code == 200:
      dados_loc = resp1.json()
      # Busca uma lista de cidades que correspondem ao nome pesquisado
      for i in dados_loc['results']:
        cidades_encontradas.append({"nome": i["name"], "latitude": i["latitude"], "longitude": i["longitude"], "estado": i['admin1'], "país": i["country"]})
      for j, k in enumerate(cidades_encontradas):
        print(f"{j + 1}) {k['nome']}, {k['estado']}, {k['país']}")
      return cidades_encontradas

    else:
      print(f'Erro {resp1.status_code} ao localizar dados')

  except Exception as e:
    print(f'Ocorreu um erro {e}')

def selecionar_cidade(cidades_encontradas):
  while True:
    try:
        entrada = input("\nCaso a cidade que você deseja seja uma dessas, digite seu número correspondente. Caso contrário, digite 0: ")
        indice_cidade = int(entrada)
        if 0 <= indice_cidade <= len(cidades_encontradas):
            break  # Sai do loop se a entrada for válida
        else:
            print("Número inválido. Por favor, tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite apenas um número.")
  if indice_cidade == 0:
    return None, None
  else:
    # Retorna a latitude e a longitude da cidade em questão
    return cidades_encontradas[indice_cidade - 1]['latitude'], cidades_encontradas[indice_cidade - 1]['longitude']


def obter_previsao(latitude, longitude):
  # URL base da API que retorna a temperatura e outras informações a partir da lat e long fornecidas
  URL = f'''https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation_probability&hourly=temperature_2m,precipitation_probability&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=5'''

  try:
    resp2 = requests.get(URL)

    if resp2.status_code == 200:
      dados_clima = resp2.json()

      temperatura_atual = dados_clima['current']['temperature_2m']
      chuva_agr = dados_clima['current']['precipitation_probability']

      print('\n***CLIMA ATUAL***')
      print(f'TEMPERATURA: {temperatura_atual}°C')
      print(f'PROBABILIDADE DE CHUVA: {chuva_agr}%')

      print("\n***PREVISÃO PARA OS PRÓXIMOS 5 DIAS***")
      for i in range(len(dados_clima['daily']['time'])):
         # Converte a string de data para um objeto datetime
         data = datetime.fromisoformat(dados_clima['daily']['time'][i])
         # Formata a data para "Nome da semana (dd/mm)
         dia_formatado = data.strftime("%A (%d/%m)").capitalize()
         temp_maxima = dados_clima["daily"]["temperature_2m_max"][i]
         temp_minima = dados_clima["daily"]["temperature_2m_min"][i]
         chance_chuva = dados_clima["daily"]["precipitation_probability_max"][i]

         print(f'{dia_formatado}')
         print(f'Máxima: {temp_maxima}°C')
         print(f'Mínima: {temp_minima}°C')
         print(f'Probabilidade de chuva: {chance_chuva}%')
         print('******')
    else:
      print(f'Erro {resp2.status_code} ao localizar dados')

  except Exception as ex:
    print(f'Ocorreu um erro {ex}')

# Execução principa - É uma convenção em Python colocar o código que executa o script dentro desse bloco
if __name__ == "__main__":
    lista_cidades = buscar_cidades()
    latitude, longitude = selecionar_cidade(lista_cidades)

    if latitude is not None and longitude is not None:
        obter_previsao(latitude, longitude)
    else:
        print("\nInfelizmente não foi possível encontrar a cidade desejada. Sentimos muito!")
