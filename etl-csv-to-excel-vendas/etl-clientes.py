import pandas as pd
import os
from datetime import datetime

"""
ETL - Análise de Clientes com Segmentação

Este script realiza um processo ETL (Extract, Transform, Load) a partir de um arquivo CSV contendo dados de clientes.
As etapas são:

1. Extração dos dados do arquivo 'clientes.csv'.
2. Transformação dos dados, incluindo:
   - Preenchimento de valores nulos em 'idade' com a média.
   - Conversão de datas para o tipo datetime.
   - Criação de uma nova coluna 'segmento_cliente' com base no total de compras:
        Baseado no valor de total_compras, você classifica o cliente em categorias:
            VIP → se total_compras ≥ 4000
            Frequente → entre 2000 e 3999
            Ocasional → < 2000
   - Cálculo dos dias desde a última compra.
   - Ordenação por total de compras em ordem decrescente.
3. Carregamento dos dados transformados em um arquivo Excel chamado 'relatorio_clientes.xlsx'.
"""


# Extração
def extrair(arquivo, caminho):
    try:
        data = pd.read_csv(os.path.join(caminho, arquivo), delimiter=',', encoding='utf-8')
    except Exception as e:
        print(f'Não foi possível extrair os dados! Erro: {e}')
    else:
        return data


# Transformação
def transformar(tabela):
    # Preenchendo os dados nulos de idade com a média das idades
    tabela['idade'] = tabela['idade'].fillna(tabela['idade'].mean())
    # Conversão da coluna ultima_compra para datetime
    tabela['ultima_compra'] = pd.to_datetime(tabela['ultima_compra'])

    # Criando coluna segmento_cliente
    def classifica_clientes(valor):
        if valor >= 4000:
            return 'VIP'
        elif valor >= 2000:
            return 'Frequente'
        else:
            return 'Ocasional'

    tabela['segmento_cliente'] = tabela['total_compras'].apply(classifica_clientes)

    # Coluna de dias desde a última compra
    data_atual = datetime.today()
    tabela['dias_desde_ultima_compra'] = (data_atual - tabela['ultima_compra']).dt.days

    # Ordenar por total_compras em ordem decrescente
    tabela_ordenada = tabela.sort_values(by='total_compras', ascending=False)

    return tabela_ordenada


# Carregamento
def carregar(caminho, arquivo, tabela):
    try:
        tabela.to_excel(os.path.join(caminho, arquivo), index=False)
    except Exception as e:
        print(f'Não foi possível carregar o arquivo! Erro: {e}')
    else:
        print(f'Arquivo salvo como "{arquivo}"')


arquivo_input = 'clientes.csv'
caminho_input = 'C:/Users/Giovana/GithHub repositorios/etls/etl-csv-to-excel-vendas/dados/input/'

df = extrair(arquivo_input, caminho_input)

df_transformado = transformar(df)

arquivo_output = 'relatorio_clientes.xlsx'
caminho_output = 'C:/Users/Giovana/GithHub repositorios/etls/etl-csv-to-excel-vendas/dados/output/'

carregar(caminho_output, arquivo_output, df_transformado)
