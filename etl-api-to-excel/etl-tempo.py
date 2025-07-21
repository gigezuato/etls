import requests
import pandas as pd


# Extração
def extrair(url):
    try:
        response = requests.get(url)
        arquivo_json = response.json()
        dados = arquivo_json['hourly']
        return dados
    except Exception as e:
        print(f'Não foi possível extrair os dados! Erro: {e}')


# Criando o dataframe a partir do json
def obtendo_dataframe(dados):
    # Renomeando as colunas
    df = pd.DataFrame({
        'Horários': dados['time'],
        'Temperatura (°C)': dados['temperature_2m'],
        'Umidade relativa do ar (%)': dados['relative_humidity_2m'],
        'Velocidade do vento (km/h)': dados['windspeed_10m']
    })
    df.set_index('Horários', inplace=True)  # Os horários serão os índices
    return df


# Transformação
def transformar(dados):
    df = obtendo_dataframe(dados)
    # Transformando Horários para tipo datetime
    df.index = pd.to_datetime(df.index)
    return df

url = "https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
dados = extrair(url)
df = transformar(dados)
print(df)
