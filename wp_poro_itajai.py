from save_to_excel import save_to_excel
import requests
from bs4 import BeautifulSoup
import pandas as pd
from keywords import keywords

base_url = 'https://www.portoitajai.com.br/licitacoes?p='

def extract_data_from_page(page_number):
    url = f"{base_url}{page_number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('li')
        data = []
        for item in items:
            a_tag = item.find('a')
            if a_tag:
                link = a_tag['href']
                credenciamento_span = a_tag.find('span', class_='bidding_number')
                if credenciamento_span:
                    credenciamento = credenciamento_span.get_text(strip=True)
                    abertura, objeto, publicado_em = None, None, None
                    spans = a_tag.find_all('span', class_='bidding_info')
                    for span in spans:
                        strong_tag = span.find('strong')
                        if strong_tag:
                            key = strong_tag.get_text(strip=True)
                            value = strong_tag.next_sibling.strip() if strong_tag.next_sibling else ''
                            if 'Abertura' in key:
                                abertura = value
                            elif 'Objeto' in key:
                                objeto = value
                            elif 'Publicado em' in key:
                                publicado_em = value
                    if credenciamento and abertura and objeto and publicado_em:
                        data.append({
                            'credenciamento': credenciamento,
                            'abertura': abertura,
                            'objeto': objeto,
                            'publicado em': publicado_em,
                            'link': f"https://www.portoitajai.com.br{link}"
                        })
        return data
    else:
        return None

all_data = []
page = 1
max_pages = 100  # Define um limite máximo de páginas para evitar loop infinito

while page <= max_pages:
    page_data = extract_data_from_page(page)
    if page_data is None or len(page_data) == 0:
        break
    all_data.extend(page_data)
    page += 1

df_completa = pd.DataFrame(all_data)
save_to_excel(df_completa, 'l_porto_itajai_completa.xlsx')
print('salvo')
