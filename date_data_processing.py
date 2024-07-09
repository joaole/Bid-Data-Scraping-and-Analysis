import pandas as pd
from datetime import datetime, timedelta
from remove_special_characters import remove_special_characters
import re

def clean_date(date_str):
    if pd.isna(date_str):
        return None  # Handle NaN values
    
    if not isinstance(date_str, str):
        date_str = str(date_str)  # Convert other types to string if necessary
    
    # Remove hours, minutes, and other irrelevant text
    date_str = re.sub(r'(\d{1,2}[:hH]\d{2}(:\d{2})?(min)?|às|do dia|h|,|:| horas| e \d{1,2} minutos| até \d{1,2}[:hH]\d{2}min? do dia| a \d{2}/\d{2}/\d{4}| das \d{1,2}[:hH]\d{2})', '', date_str)
    date_str = re.sub(r'\b\d{1,2}h\b', '', date_str)  # Remove standalone hours like "10h"
    date_str = re.sub(r'(\d{1,2}[:hH]\d{2}min?|\d{1,2}[:hH]\d{2})', '', date_str)  # Remove complete hours like "09h30min"
    date_str = re.sub(r'\(.*?\)', '', date_str)  # Remove parentheses and their contents
    date_str = re.sub(r'\s+', ' ', date_str).strip()  # Remove extra spaces
    date_str = re.sub(r'\b\d{2}/\d{2}/\d{4}\b', '', date_str)  # Remove standalone numbers like "10 28/06/2024"
    
    return date_str

def process_data(file_path):
    df = load_data(file_path)
    df['Objetivo'] = df['Objetivo'].astype(str).apply(remove_special_characters)
    df['DataAbertura'] = df['DataAbertura'].apply(clean_date)
    df['DataAbertura'] = pd.to_datetime(df['DataAbertura'], errors='coerce')  # Convert all dates that are not yet in datetime format
    filtered_df = filter_data_by_keywords_and_date(df, keywords)
    return filtered_df

def load_data(file_path):
    return pd.read_excel(file_path)

def filter_data_by_keywords_and_date(df, keywords):
    start_date = datetime.now() - timedelta(days=30)
    filtered_data = df[df.apply(lambda row: any(keyword in row['Objetivo'] for keyword in keywords) and row['DataAbertura'] >= start_date, axis=1)]
    return filtered_data

# Sample keywords list
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
    "basic design", "executive design", "detailed design", "gerenciamento de obras", "gerenciamento de obra", "supervisao e acompanhamento de obras",
    "planejamento estrategico", "plano de negocios", "plano de negocio", "planos mestres", "plano mestre", "planos de investimentos",
    "plano de investimento", "plano de gestao e monitoriamento", "planos diretores", "plano diretor", "estudos ambientais",
    "estudo ambiental", "gestao continuada", "planos e programas", "plano e programa", "eia", "rima"
]
