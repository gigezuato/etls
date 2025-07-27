import requests
import pandas as pd
import numpy as np
import os


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
        'temperatura': dados['temperature_2m'],
        'umidade_relativa_ar': dados['relative_humidity_2m'],
        'velocidade_vento': dados['windspeed_10m']
    })

    df.set_index('horários', inplace=True)  # Os horários serão os índices

    # Transformando Horários para tipo datetime
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize('UTC').tz_convert('America/Sao_Paulo')  # Convertendo para horário local

    # Obter dados de uma semana, contando a partir do dia atual
    hoje = pd.Timestamp.now(tz='America/Sao_Paulo').normalize()
    fim = hoje + pd.Timedelta(days=7)
    df = df.loc[(df.index >= hoje) & (df.index < fim)]

    return df


# Criando colunas clima (classifica o clima) e periodo_dia (classifica os horários)
def classifica_clima_e_horarios(df):
    # Clima
    condicoes_clima = [df['temperatura'] < 15, (df['temperatura'] >= 15) & (df['temperatura'] <= 25)]
    classificacoes_clima = ['Frio', 'Ameno']

    df['clima'] = np.select(condicoes_clima, classificacoes_clima, default='Quente')

    # Horários
    condicoes_horarios = [(df.index.hour >= 6) & (df.index.hour < 12),
                          (df.index.hour >= 12) & (df.index.hour < 18),
                          (df.index.hour >= 18) & (df.index.hour < 23)]
    classificacoes_horarios = ['Manhã', 'Tarde', 'Noite']

    df['periodo_dia'] = np.select(condicoes_horarios, classificacoes_horarios, 'Madrugada')

    return df


def exportar(arquivo, caminho, df):
    try:
        df.index = df.index.tz_convert(None)
        df.to_excel(os.path.join(caminho, arquivo), index=True)
    except Exception as e:
        print(f'Não foi possível exportar o arquivo! Erro: {e}')
    else:
        print(f'Arquivo salvo como {arquivo}!')


url = "https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
dados = extrair(url)
df = obtendo_dataframe(dados)
df_final = classifica_clima_e_horarios(df)
arquivo_output = 'previsao_tempo.xlsx'
caminho_output = 'C:/Users/Giovana/GithHub repositorios/etls/etl-api-to-excel/dados/output/'
exportar(arquivo_output, caminho_output, df_final)