"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv(
        "files/input/solicitudes_de_credito.csv",
        sep=";",
        index_col=0
    )
    # 1. Limpieza de columnas tipo texto (object)
    text_cols = df.select_dtypes(include=["object"]).columns

    for col in text_cols:
        df[col] = (
            df[col]
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace(".00", "", regex=False)
        )
    #2Conversión de tipos numéricos
    df["monto_del_credito"] = df["monto_del_credito"].astype(float)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    # 3. Corrección del formato de fecha
    #    Algunos registros están en formato dd/mm/YYYY, otros YYYY/mm/dd
    fecha = df["fecha_de_beneficio"]

    fecha_1 = pd.to_datetime(fecha, format="%d/%m/%Y", errors="coerce")
    fecha_2 = pd.to_datetime(fecha, format="%Y/%m/%d", errors="coerce")

    # Combina el que sirva (el primero no nulo)
    df["fecha_de_beneficio"] = fecha_1.combine_first(fecha_2)
    # 4. Eliminación de duplicados y na
    df = df.drop_duplicates()
    df = df.dropna()
    # 5. Guardado del resultado
    os.makedirs("files/output", exist_ok=True)

    df.to_csv(
        "files/output/solicitudes_de_credito.csv",
        index=False,
        sep=";",
        encoding="utf-8"
    )
     

