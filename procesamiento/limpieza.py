from __future__ import annotations

import pandas as pd


COLUMNAS_NUMERICAS = [
    "idpeaje",
    "valortarifa",
    "cantidadtrafico",
    "cantidadevasores",
    "cantidadexentos787",
]

COLUMNAS_OBLIGATORIAS = [
    "idpeaje",
    "peaje",
    "categoriatarifa",
    "desde",
    "hasta",
    "valortarifa",
    "cantidadtrafico",
    "cantidadevasores",
    "cantidadexentos787",
]


def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    datos = df.copy()
    datos.columns = [columna.lower() for columna in datos.columns]
    columnas_faltantes = [columna for columna in COLUMNAS_OBLIGATORIAS if columna not in datos.columns]
    if columnas_faltantes:
        raise ValueError(
            "La respuesta de la API no contiene las columnas esperadas: "
            + ", ".join(columnas_faltantes)
        )

    for columna in COLUMNAS_NUMERICAS:
        if columna in datos.columns:
            serie = pd.to_numeric(datos[columna], errors="coerce").fillna(0)
            datos[columna] = pd.to_numeric(serie, downcast="integer")

    for columna in ["desde", "hasta"]:
        if columna in datos.columns:
            datos[columna] = pd.to_datetime(datos[columna], errors="coerce")

    datos["categoria_tarifa"] = datos["categoriatarifa"].fillna("Sin categoria")
    datos["ingreso_estimado"] = datos["cantidadtrafico"] * datos["valortarifa"]
    datos["periodo"] = datos["hasta"].dt.to_period("M").dt.to_timestamp()
    datos["anio"] = pd.to_numeric(datos["hasta"].dt.year, downcast="integer")
    datos["mes"] = datos["hasta"].dt.strftime("%Y-%m").astype("category")
    datos["tasa_evasion"] = (
        datos["cantidadevasores"]
        / (datos["cantidadtrafico"] + datos["cantidadevasores"]).replace(0, pd.NA)
    ).fillna(0).astype("float32")
    datos["porcentaje_exentos"] = (
        datos["cantidadexentos787"]
        / (datos["cantidadtrafico"] + datos["cantidadexentos787"]).replace(0, pd.NA)
    ).fillna(0).astype("float32")

    for columna in ["peaje", "categoriatarifa", "categoria_tarifa"]:
        if columna in datos.columns:
            datos[columna] = datos[columna].fillna("Sin dato").astype("category")

    datos["ingreso_estimado"] = pd.to_numeric(datos["ingreso_estimado"], downcast="integer")

    return datos.sort_values(["hasta", "peaje", "categoria_tarifa"]).reset_index(drop=True)
