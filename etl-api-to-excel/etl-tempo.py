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
        'horários': dados['time'],
        'temperatura (°C)': dados['temperature_2m'],
        'umidade relativa do ar (%)': dados['relative_humidity_2m'],
        'velocidade do vento (km/h)': dados['windspeed_10m']
    })

    df.set_index('horários', inplace=True)  # Os horários serão os índices

    # Transformando Horários para tipo datetime
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize('UTC').tz_convert('America/Sao_Paulo')  # Convertendo para horário local

    # Obter dados de uma semana, contando a partir do dia atual
    hoje = pd.Timestamp.now(tz='America/Sao_Paulo')
    fim = hoje + pd.Timedelta(days=7)  # Uma semana
    df = df.loc[(df.index >= hoje) & (df.index <= fim)]
    return df


url = "https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
dados = extrair(url)
df = obtendo_dataframe(dados)
print(df)
