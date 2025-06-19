import pandas as pd
import os
"""
ETL - Leitura de arquivo CSV com vendas, transformação dos dados e exportação para Excel.
Transformações aplicadas:
- Criação de coluna 'total_venda'
- Conversão de datas
- Ordenação decrescente por data
"""

arquivo_input = 'vendas.csv'
caminho_input = 'C:/Users/Giovana/GithHub repositorios/etls/etl-csv-to-excel-vendas/dados/input/'

# Extração

df = pd.read_csv(os.path.join(caminho_input, arquivo_input), delimiter=',', encoding='utf-8')

# Transformação

# Criar a nova coluna total_venda
df['total_venda'] = df['preco_unitario'] * df['quantidade']
# Converter a coluna data_venda para data
df['data_venda'] = pd.to_datetime(df['data_venda'])
# Ordenar o DataFrame pelo campo data_venda em ordem decrescente
df_ordenado = df.sort_values(by='data_venda', ascending=False)

# Carregamento
arquivo_output = 'relatorio_vendas.xlsx'
caminho_output = 'C:/Users/Giovana/GithHub repositorios/etls/etl-csv-to-excel-vendas/dados/output/'
df_ordenado.to_excel(os.path.join(caminho_output, arquivo_output), index=False)
print('ETL concluída com sucesso!')