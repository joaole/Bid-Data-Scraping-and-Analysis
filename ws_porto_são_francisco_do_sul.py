import requests
from bs4 import BeautifulSoup
import pandas as pd
from remove_special_characters import remove_special_characters
from save_to_excel import save_to_excel
from keywords import keywords

def keywords_filter(df, keywords):
    pattern = '|'.join(keywords)
    return df[df['Objetivo'].str.contains(pattern, case=False, na=False)]

# URL da página para scraping
url = 'https://portosaofrancisco.com.br/licitacoes/'

# Headers para a requisição HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazer a requisição HTTP
response = requests.get(url, headers=headers)

if response.status_code == 200:
    site = BeautifulSoup(response.text, 'html.parser')
    containers = site.findAll('div', attrs={'class': 'col-sm-12 dados'})
    
    data_completa = []
    
    for container in containers:
        data = container.findAll('div', attrs={'class':'col-sm-12'})
        row = [d.get_text(strip=True) for d in data]
        link_edital = container.find('a', href=True)['href'] if container.find('a', href=True) else ''
        row.append(link_edital)
        data_completa.append(row)

    max_columns = max(len(row) for row in data_completa)
    colunas = ['Modalidade', 'Edital', 'DataAbertura', 'Objetivo', '', '', 'Link']
    
    for row in data_completa:
        while len(row) < max_columns:
            row.append('')

    df_completa = pd.DataFrame(data_completa, columns=colunas)
    df_completa = df_completa.applymap(remove_special_characters)
    df_tratada = keywords_filter(df_completa, keywords)
    
    save_to_excel(df_completa, 'Licitacoes_porto_são_Francisco_COMPLETA.xlsx')
    save_to_excel(df_tratada, 'Licitacoes_porto_são_Francisco_TRATADA.xlsx')

    print('Licitacoes processadas e salvas com sucesso.')
else:
    print(f"Falha ao buscar a página. Código de status: {response.status_code}")
