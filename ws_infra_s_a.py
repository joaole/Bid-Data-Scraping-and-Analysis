import requests
from bs4 import BeautifulSoup
import pandas as pd
from save_to_excel import save_to_excel

# URL da página para scraping
url = 'https://www.infrasa.gov.br/licitacoes/'

# Fazer a requisição HTTP
response = requests.get(url)

if response.status_code == 200:
    site = BeautifulSoup(response.text, 'html.parser')

    # Localizar a tabela
    tabela = site.find('table', attrs={'id': 'table_1'})

    if tabela:
        # Extrair as linhas da tabela
        rows = tabela.findAll('tr')

        # Extrair dados de cada linha
        data_bruta = []
        for row in rows:
            cells = row.findAll('td')
            if cells:  # Verificar se a linha possui células
                cells = [cell.get_text(strip=True) for cell in cells]
                data_bruta.append(cells)

        # Determinar o número de colunas com base na primeira linha
        num_columns = len(data_bruta[0]) if data_bruta else 0

        # Definir nomes das colunas com base no número de colunas presentes
        columns = ['Data da Publicação', 'Título', 'Nº da licitação', 'Modalidade', 'DataAbertura', 'Objetivo', 'Situação', 'Empresa', 'Data'][:num_columns]

        # Criar DataFrame completo
        try:
            df_completa = pd.DataFrame(data_bruta, columns=columns)
        
            save_to_excel(df_completa, 'Licitações_infrasa_completa.xlsx')
            print("Dados completos salvos e formatados em Licitações_infrasa_completa.xlsx")

        except ValueError as e:
            print(f"Erro ao criar DataFrame: {e}")

        df_tratada = df_completa.drop(['Data da Publicação', 'Título', 'Nº da licitação', 'Modalidade', ])
    else:
        print("Tabela não encontrada na página.")
else:
    print(f"Falha ao buscar a página. Código de status: {response.status_code}")
