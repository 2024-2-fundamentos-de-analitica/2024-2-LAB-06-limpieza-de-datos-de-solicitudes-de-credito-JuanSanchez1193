"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
from datetime import datetime
import re

from datetime import datetime
def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    """
    file = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df = file.copy()
    
    df = df.dropna()
    
    df["sexo"] = df["sexo"].str.lower()

    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()

    df["sexo"] = df["sexo"].str.lower()

    df = df.dropna()

    df["idea_negocio"] = df["idea_negocio"].str.lower().str.replace("-"," ").str.replace("_"," ")

    df["barrio"] = df["barrio"].str.lower().str.replace("-"," ").str.replace("_"," ")

    df["estrato"] = df["estrato"].astype(int)
    df["idea_negocio"] = df["idea_negocio"].str.lower().str.replace("-"," ").str.replace("_"," ")

    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    df["fecha_de_beneficio"] = [
        (
            datetime.strptime(date, "%d/%m/%Y")
            if bool(re.search(r"\d{1,2}/\d{2}/\d{4}", date))
            else datetime.strptime(date, "%Y/%m/%d")
        )

        for date in df["fecha_de_beneficio"]
        ]
    
    df["monto_del_credito"] = df["monto_del_credito"].str.strip("$").str.replace(r"\.00", "", regex=True).str.replace(",","").astype(int)
    df["línea_credito"] = df["línea_credito"].str.strip().str.lower().str.replace("-", " ").str.replace("_", " ").str.replace(". ", ".")
    
    df = df.drop_duplicates()
    df["línea_credito"] = df["línea_credito"].str.strip().str.lower().str.replace("-", " ").str.replace("_", " ").str.replace(". ", ".")
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=True)


pregunta_01()