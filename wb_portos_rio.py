import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import unidecode
from save_to_excel import save_to_excel

def remove_special_characters(text):
    if isinstance(text, str):
        return unidecode.unidecode(text.lower())
    return text

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
    "simulacoes operacionais", "simulacao operacional", "macro e microssimulacao de transporte", "estudos de logistica", "estudo de logistica",
    "sustentabilidade", "avaliacoes de mercados", "avaliacao de mercado", "avaliacoes de mercados", "previsoes e cenarios", "previsoes", "cenarios",
    "estruturacao de projetos", "basic design", "executive design", "detailed design", "gerenciamento de obras", "gerenciamento de obra",
    "supervisao e acompanhamento de obras", "planejamento estrategico", "plano de negocios", "plano de negocio", "planos mestres", "plano mestre",
    "planos de investimentos", "plano de investimento", "plano de gestao e monitoriamento", "planos diretores", "plano diretor", "estudos ambientais",
    "estudo ambiental", "gestao continuada", "planos e programas", "plano e programa", "eia", "rima"
]

def filter_data_by_keywords(df, keywords):
    if 'objeto' not in df.columns:
        print("A coluna 'objeto' não foi encontrada no DataFrame.")
        return pd.DataFrame()  # Retorna um DataFrame vazio se a coluna não existir
    return df[df['objeto'].apply(lambda x: any(keyword in x for keyword in keywords))]

# Inicializar o webdriver (certifique-se de especificar o caminho correto para o seu driver)
driver = webdriver.Chrome()

try:
    # Abrir a página desejada
    driver.get('https://transparencia.portosrio.gov.br/relatorio/tp/licitacao')

    # Esperar o elemento estar presente
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.jss83'))
    )
    
    soup = BeautifulSoup((elements.__getattribute__('innerHTML')), 'html.parser' )


except selenium.common.exceptions.TimeoutException:
    print("O elemento não foi encontrado dentro do período de tempo.")
finally:
    # Fechar o webdriver
    driver.quit()
