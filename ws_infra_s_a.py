import requests
from bs4 import BeautifulSoup
import pandas as pd
from save_to_excel import save_to_excel
from remove_special_characters import remove_special_characters
from keywords import keywords

def keywords_filter(df, keywords):
    pattern = '|'.join(keywords)
    return df[df['Objeto'].str.contains(pattern, case=False, na=False)]

# URL da página para scraping
url = 'https://www.infrasa.gov.br/licitacoes/'

# Headers para a requisição HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazer a requisição HTTP
response = requests.get(url, headers=headers)

if response.status_code == 200:
    site = BeautifulSoup(response.text, 'html.parser')
    table = site.find('table', {'id': 'table_1'})

    # Extraindo cabeçalhos das colunas
    headers = [header.get_text(strip=True) for header in table.find_all('th')]

    # Extraindo dados das linhas
    data = []
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        data.append([col.get_text(strip=True) for col in cols])

    # Criando o DataFrame
    df_completo = pd.DataFrame(data, columns=headers)
    df_completo = df_completo.map(remove_special_characters)
    
    # Salvando em um arquivo Excel
    save_to_excel(df_completo, 'licitacoes_infrasa_completo.xlsx')

    # Filtrar por Situação
    situacao_filtro = "em andamento"
    df_filtrado = df_completo[df_completo['Situação'] == situacao_filtro]
    df_filtrado = keywords_filter(df_filtrado, keywords)

    save_to_excel(df_filtrado, 'licitacoes_infra_tratada.xlsx')
    
else:
    print(f"Falha ao buscar a página. Código de status: {response.status_code}")
