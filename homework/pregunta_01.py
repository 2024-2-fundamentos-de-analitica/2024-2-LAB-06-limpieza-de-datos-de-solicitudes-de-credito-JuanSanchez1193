import pandas as pd
import re
from fuzzywuzzy import process

def limpieza_sexo_idea_negocio(df):
    columnas_texto = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']
    for col in columnas_texto:
        df[col] = df[col].str.lower().str.strip()
        df[col] = df[col].apply(lambda x: re.sub(r'[-_]', ' ', x) if pd.notnull(x) else x)
    return df

def normalizar_barrio(df):
    barrios_unicos = df['barrio'].dropna().unique()
    mapeo_barrios = {}
    
    for barrio in barrios_unicos:
        if not mapeo_barrios:  # Si el diccionario está vacío, agregar el primer barrio
            mapeo_barrios[barrio] = barrio
            continue
        
        mejor_coincidencia = process.extractOne(barrio, mapeo_barrios.keys())
        if mejor_coincidencia and mejor_coincidencia[1] > 85:  # Si hay una coincidencia alta
            mapeo_barrios[barrio] = mejor_coincidencia[0]
        else:
            mapeo_barrios[barrio] = barrio
    
    df['barrio'] = df['barrio'].map(mapeo_barrios)
    return df

def limpiar_monto_credito(df):
    df['monto_del_credito'] = df['monto_del_credito'].astype(str)
    df['monto_del_credito'] = df['monto_del_credito'].apply(lambda x: re.sub(r'[^0-9]', '', x))
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    df.dropna(subset=['monto_del_credito'], inplace=True)
    return df

def normalizar_linea_credito(df):
    df['línea_credito'] = df['línea_credito'].str.lower().str.strip()
    df['línea_credito'] = df['línea_credito'].apply(lambda x: re.sub(r'\s+', ' ', x) if pd.notnull(x) else x)
    return df

def limpiar_solicitudes_credito(input_file, output_file):
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    
    df = limpieza_sexo_idea_negocio(df)
    df = normalizar_barrio(df)
    df = limpiar_monto_credito(df)
    df = normalizar_linea_credito(df)
    
    if 'result' in df.columns:
        df.drop(columns=['result'], inplace=True)
    
    # Eliminar cualquier columna cuyo nombre comience con 'Unnamed'
    df.drop(columns=[col for col in df.columns if col.startswith('Unnamed')], inplace=True)
    
    columnas_criticas = ['sexo', 'tipo_de_emprendimiento', 'barrio', 'estrato', 'comuna_ciudadano', 'fecha_de_beneficio', 'monto_del_credito']
    df.dropna(subset=columnas_criticas, inplace=True)
    
    df['fecha_de_beneficio'] = pd.to_datetime(df['fecha_de_beneficio'], errors='coerce')
    df.dropna(subset=['fecha_de_beneficio'], inplace=True)
    
    df.drop_duplicates(inplace=True)
    
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(df['sexo'].value_counts().to_list())

def pregunta_01():
    limpiar_solicitudes_credito("files/input/solicitudes_de_credito.csv", "files/output/solicitudes_de_credito.csv")

pregunta_01()









import pandas as pd

def imprimir_valores_unicos(input_file):
    # Cargar el archivo CSV
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')

    # Recorrer cada columna e imprimir sus valores únicos
    for col in df.columns:
        print(f"Columna: {col}")
        print(df[col].dropna().unique())  # Imprime los valores únicos, ignorando los nulos
        print("-" * 50)

# Llamada a la función
imprimir_valores_unicos("files/output/solicitudes_de_credito.csv")
