from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
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
    if isinstance(text, str):
        return any(keyword in text for keyword in keywords)
    return False

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the URL
url = "https://portaldecompras.sc.gov.br/#/"
driver.get(url)

# Wait for the page to load completely
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "table"))
)

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

# Find all tables on the page
tables = soup.find_all('table', class_='table')

# List to store all table data
all_data = []

# Extract data from each table
for table in tables:
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')[1:]  # Skip the header row

    # Extract row data
    for row in rows:
        cells = row.find_all(['td', 'th'])  # Include 'th' for the first column
        row_data = [str(cell.text.strip()) for cell in cells]
        all_data.append(dict(zip(headers, row_data)))

# Convert to DataFrame
combined_df = pd.DataFrame(all_data)

df_tratada = combined_df.copy()

# Ensure all entries in "Descrição do Objeto" are strings and handle NaN values
df_tratada["Descrição do Objeto"] = df_tratada["Descrição do Objeto"].astype(str).fillna('')

df_tratada["Descrição do Objeto"] = df_tratada["Descrição do Objeto"].apply(remove_special_characters)
df_tratada["Descrição do Objeto"] = df_tratada["Descrição do Objeto"].apply(lambda x: keywords_filter(x, keywords))

# Display the DataFrame
save_to_excel(combined_df, 'licitações_portal_de_compras_completo.xlsx')
save_to_excel(df_tratada, 'licitações_portal_de_compras_tratada.xlsx')
