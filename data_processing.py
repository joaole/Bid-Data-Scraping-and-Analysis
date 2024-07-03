import pandas as pd
from datetime import datetime, timedelta
import re

def remove_special_characters(text):
    if pd.isna(text):
        return text
    return ''.join(e for e in str(text) if e.isalnum() or e.isspace())

# Lista de palavras-chave formatadas
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
    "basic design", "executive designs", "executive design", "construction management", "construction supervision and monitoring",
    "strategic planning", "business plan", "master plans", "master plan", "investment plans", "investment plan", "management and monitoring plan",
    "environmental studies", "environmental study", "continuous management", "plans and programs", "plan and program",
    "environmental impact study and report eia rima", "environmental impact study", "environmental impact report", "eia", "rima",
    "regulatory evaluations", "regulatory evaluation", "public hearing materials", "public hearing material", "technical reports",
    "technical report", "service adequacy evaluation", "operational evaluations", "operational evaluation", "capacity evaluation",
    "operational performance evaluation"
]

def load_data(file_path):
    """Carrega os dados do arquivo Excel."""
    return pd.read_excel(file_path)

def clean_date(date_str):
    """Limpa e formata a string de data para um formato padrão."""
    if pd.isna(date_str):
        return date_str
    if isinstance(date_str, pd.Timestamp):
        return date_str

    # Mantém a string original para fins de depuração
    original_date_str = date_str

    # Remover horas, minutos e outros textos irrelevantes
    date_str = re.sub(r'(\d{1,2}[:hH]\d{2}(:\d{2})?(min)?|às|do dia|h|,|:| horas| e \d{1,2} minutos| até \d{1,2}[:hH]\d{2}min? do dia| a \d{2}/\d{2}/\d{4}| das \d{1,2}[:hH]\d{2})', '', date_str)
    date_str = re.sub(r'\b\d{1,2}h\b', '', date_str)  # Remove horas soltas como "10h"
    date_str = re.sub(r'(\d{1,2}[:hH]\d{2}min?|\d{1,2}[:hH]\d{2})', '', date_str)  # Remove horas completas como "09h30min"
    date_str = re.sub(r'\(.*?\)', '', date_str)  # Remove parênteses e seu conteúdo
    date_str = re.sub(r'\s+', ' ', date_str).strip()  # Remove espaços extras

    # Verificação adicional para ver se a string resultante ainda contém dígitos
    if not re.search(r'\d', date_str):
        print(f"Data inválida após limpeza: {original_date_str} -> {date_str}")
        return pd.NaT

    print(f"Original: {original_date_str}, Cleaned: {date_str}")  # Depuração adicional

    # Tentativa de diferentes formatos de data
    date_formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d", "%d/%m/%y", "%d-%m-%y", "%m/%d/%Y", "%m-%d-%Y", "%d %m %Y"]
    for fmt in date_formats:
        try:
            return pd.to_datetime(date_str, format=fmt, errors='coerce')
        except ValueError:
            continue

    # Se todas as tentativas falharem, retorna a string original para fins de depuração
    return original_date_str

def filter_data_by_keywords_and_date(df, keywords, days=30):
    """Filtra os dados com base nas palavras-chave e data de abertura nos últimos X dias."""
    current_date = datetime.now()
    start_date = current_date - timedelta(days=days)

    # Padronizar os textos na coluna 'Objetivo'
    df.loc[:, 'Objetivo'] = df['Objetivo'].apply(remove_special_characters)

    # Exibir valores originais da coluna 'DataAbertura' antes da limpeza
    print("Valores originais da coluna 'DataAbertura':")
    print(df['DataAbertura'].head(20))

    # Limpar e converter as datas na coluna 'DataAbertura'
    df['DataAbertura'] = df['DataAbertura'].apply(clean_date)

    # Exibir valores convertidos da coluna 'DataAbertura' após a limpeza
    print("Valores convertidos da coluna 'DataAbertura':")
    print(df['DataAbertura'].head(20))

    # Identificar e exibir datas não reconhecidas
    unrecognized_dates = df[df['DataAbertura'].apply(lambda x: isinstance(x, str))]
    if not unrecognized_dates.empty:
        print("Datas não reconhecidas:")
        print(unrecognized_dates[['DataAbertura', 'Objetivo']])

    # Converta todas as datas que ainda não estão no formato datetime
    df['DataAbertura'] = pd.to_datetime(df['DataAbertura'], errors='coerce')

    # Verifica se a coluna 'DataAbertura' foi convertida corretamente
    if df['DataAbertura'].isnull().any():
        problematic_rows = df[df['DataAbertura'].isnull()]
        print("Valores problemáticos na coluna 'DataAbertura':")
        print(problematic_rows[['DataAbertura', 'Objetivo']])
        raise ValueError("Existem valores nulos na coluna 'DataAbertura' após a conversão. Verifique o formato das datas.")

    # Filtrar as linhas que contêm palavras-chave e cuja data de abertura está dentro dos últimos 30 dias
    filtered_data = df[df.apply(lambda row: any(keyword in row['Objetivo'] for keyword in keywords) and
                                          start_date <= row['DataAbertura'] <= current_date, axis=1)]
    return filtered_data

def process_data(input_file_path):
    """Processa os dados carregando e filtrando com base nas palavras-chave e data de abertura."""
    # Carregar os dados
    df = load_data(input_file_path)

    # Filtrar os dados com base nas palavras-chave e data de abertura
    filtered_df = filter_data_by_keywords_and_date(df, keywords)

    return filtered_df

# Testando o código com o arquivo fornecido
input_file_path = 'Licitações_INFRASA_completa.xlsx'
try:
    processed_data = process_data(input_file_path)
    print("Dados processados com sucesso!")
    print(processed_data.head())
except ValueError as e:
    print(e)