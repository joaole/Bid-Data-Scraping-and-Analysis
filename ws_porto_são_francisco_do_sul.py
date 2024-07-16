import requests
from bs4 import BeautifulSoup
import pandas as pd
from remove_special_characters import remove_special_characters
from save_to_excel import save_to_excel

keywords = [
    "evtea", "projeto basico", "executivo", "conceitual", "economico", "meio ambiente", "consultoria", "engenharia consultiva",
    "estruturacao de projetos", "estudos de viabilidade", "conceitual de projetos de infraestrutura", "estudo de pre-viabilidade",
    "estudo de viabilidade tecnico economico ambiental", "projetos conceituais", "projeto conceitual", "projetos basicos",
    "projeto basico", "projetos executivos", "projeto executivo", "gerenciamento de obras", "gerenciamento de obra",
    "supervisao e acompanhamento de obras", "planejamento estrategico", "plano de negocios", "plano de negocio", "planos mestres",
    "plano mestre", "planos de investimentos", "plano de investimento", "plano de gestao e monitoriamento", "planos diretores",
    "plano diretor", "estudos ambientais", "estudo ambiental", "gestao continuada", "planos e programas", "plano e programa",
    "estudo de impacto ambiental e relatorio de impacto ambiental eia/rima", "estudo de impacto ambiental", "relatorio de impacto ambiental",
    "eia", "rima", "avaliacoes regulatorias", "avaliacao relatoria", "materiais de audiencias publicas", "material de audiencia publica",
    "pareceres tecnicos", "parecer tecnico", "avaliacao de adequacao de atendimentos", "avaliacoes operacionais", "avaliacao operacional",
    "avaliacao de capacidade", "avaliacao de desempenho operacional", "planos de expansao", "plano de expansao", "monitoriamento da eficiencia",
    "simulacoes operacionais", "simulacao operacional", "macro e microssimulacao de transporte", "macro", "macro simulacao",
    "microssimulacao", "microssimulacao operacional", "estudos economicos", "analises conjunturais", "analise conjuntural",
    "avaliacao de mercado", "avaliacoes de mercados", "previsoes e cenarios", "previsoes", "cenarios", "estruturacao de projetos",
    "plano de investimentos", "plano de gestao e monitoriamento", "planos diretores", "plano diretor", "estudos ambientais",
    "estudo ambiental", "gestao continuada", "planos e programas", "plano e programa", "eia", "rima", "licitatório",  'estudos tecnicos'
]

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
