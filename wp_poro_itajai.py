import pandas as pd
from bs4 import BeautifulSoup
import requests
from save_to_excel import save_to_excel
from remove_special_characters import remove_special_characters

# Lista de palavras-chave
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
    "avaliacao de mercado", "avaliacoes de mercados", "previsoes e cenarios", "previsoes", "cenarios", "estruturacao de projetos de infraestrutura"
]

def keywords_filter(text, keywords):
    return any(keyword in text for keyword in keywords)

url = 'https://www.portoitajai.com.br/licitacoes/'

try:
    response = requests.get(url)
    response.raise_for_status()  # Levanta uma exceção para códigos de status de resposta HTTP 4xx/5xx

    site = BeautifulSoup(response.text, 'html.parser')
    soup = site.find('ul', attrs={'id': 'list_biddings'})
    if not soup:
        raise ValueError('Estrutura HTML Alterada.')

    content = soup.find_all('li')
    if not content:
        raise ValueError('Estrutura HTML Alterada ou Lista de Licitações Vazia.')

    data = []
    for li in content:
        li_data = li.find_all('span')
        li_data_individual = [d.text.strip() for d in li_data]

        link = li.find('a')
        li_data_individual.append(link['href'])
        data.append(li_data_individual)

    df_completa = pd.DataFrame(data, columns=['Modalidade', 'Abertura', 'Situação', 'Objeto', 'Publicação', 'Link'])
    save_to_excel(df_completa, 'porto_itajai_completa.xlsx')

    df_tratada = df_completa.drop(columns=['Modalidade', 'Publicação'])
    df_tratada['Objeto'] = df_tratada['Objeto'].apply(remove_special_characters)

    # Aplicar a função à coluna 'Objeto'
    df_tratada['filtered'] = df_tratada['Objeto'].apply(lambda x: keywords_filter(x, keywords))

    # Filtrar o DataFrame com base na coluna 'filtered'
    df_filtrada = df_tratada[df_tratada['filtered']]

    # Remover a coluna 'filtered' do DataFrame final
    df_filtrada = df_filtrada.drop(columns=['filtered'])

    save_to_excel(df_filtrada, 'porto_itajai_tratada.xlsx')

except requests.RequestException as e:
    print(f'Erro de conexão: {e}')
except ValueError as e:
    print(f'Erro nos dados: {e}')
except Exception as e:
    print(f'Erro inesperado: {e}')
