import requests
from bs4 import BeautifulSoup
import pandas as pd
from date_data_processing import process_data
from remove_special_characters import remove_special_characters
from save_to_excel import save_to_excel

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
    data_tratada = []
    
    for container in containers:
        data = container.findAll('div', attrs={'class':'col-sm-12'})
        row = [remove_special_characters([d.get_text(strip=True)])[0] for d in data]
        link_edital = container.find('a', href=True)['href'] if container.find('a', href=True) else ''
        row.append(link_edital)
        data_completa.append(row)

    max_columns = max(len(row) for row in data_completa)
    colunas = ['Modalidade', 'Edital', 'DataAbertura', 'Objetivo', 'Link Edital'] + [f'Column {i+1}' for i in range(5, max_columns)]
    
    for row in data_completa:
        while len(row) < max_columns:
            row.append('')

    df_completa = pd.DataFrame(data_completa, columns=colunas)
    df_tratada = pd.DataFrame(data_tratada, columns=colunas).apply(process_data)
    
    save_to_excel(df_completa, 'Licitacoes_porto_são_Francisco_COMPLETA.xlsx')
    save_to_excel(df_tratada, 'Licitacoes_porto_são_Francisco_TRATADA.xlsx')

    print('Licitacoes processadas e salvas com sucesso.')
else:
    print(f"Falha ao buscar a página. Código de status: {response.status_code}")
