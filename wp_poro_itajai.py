from bs4 import BeautifulSoup
import requests
import pandas as pd
from save_to_excel import save_to_excel

url = 'https://www.portoitajai.com.br/licitacoes/'

response = requests.get(url)

if response.status_code == 200:
    site = BeautifulSoup(response.text, 'html.parser')
    soup = site.find('ul', attrs={'id':'list_biddings'})
    content = soup.find_all('li')
    if soup and content:
        data = []

        for li in content:
            li_data = li.find_all('span')
            li_data_individual = [d.text.strip() for d in li_data]
            
            link = li.find('a')
            li_data_individual.append(link['href'])
            data.append(li_data_individual)

        df_completa = pd.DataFrame(data, columns=['Modalidade','Abertura','Situação', 'Objeto', 'Publicação', 'Link'])
        save_to_excel(df_completa, 'porto_itajai_completa.xlsx')

        
    else: 
        print('Falha ao Estrutura HTML Alterada.')
else:
    print(f'falha ao tentar conectar ao site: {response.status_code}')