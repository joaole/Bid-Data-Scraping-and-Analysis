import pandas as pd

def parse_date(date_str):
    if pd.isna(date_str):
        return date_str  # Retorna NaN como está
    if isinstance(date_str, pd.Timestamp):
        return date_str  # Retorna o Timestamp como está
    
    date_formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d", 
        "%d/%m/%y", "%d-%m-%y", "%m/%d/%Y", "%m-%d-%Y", "%d %m %Y"
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = pd.to_datetime(date_str, format=fmt, errors='coerce')
            if not pd.isna(parsed_date):
                return parsed_date
        except ValueError:
            continue
    
    return date_str  # Retorna o valor original se nenhuma conversão for bem-sucedida

# Exemplo de uso:
data = {
    'date_column': ['10/06/2023', '25-06-2023', '2023/07/01', 'not_a_date', None, pd.Timestamp('2023-07-01')]
}
df = pd.DataFrame(data)

# Aplicando a função à coluna
df['processed_date'] = df['date_column'].apply(parse_date)

print(df)
