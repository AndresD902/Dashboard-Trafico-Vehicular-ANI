from __future__ import annotations

import pandas as pd
import streamlit as st

from datos.cliente_api import ClienteAPI
from procesamiento.limpieza import preparar_datos
from procesamiento.transformaciones import aplicar_filtros


@st.cache_data(show_spinner="Consultando la API publica de peajes...")
def cargar_datos() -> pd.DataFrame:
    cliente = ClienteAPI()
    try:
        datos_crudos = cliente.obtener_registros()
    except RuntimeError as error:
        raise RuntimeError(str(error)) from error

    if datos_crudos.empty:
        raise ValueError("La API respondio correctamente, pero no devolvio registros.")

    return preparar_datos(datos_crudos)


def cargar_datos_filtrados(
    peajes: list[str],
    categorias: list[str],
    rango_fechas: tuple[pd.Timestamp, pd.Timestamp] | None,
    anios: list[int] | None = None,
    proporcion_registros: float = 1.0,
) -> pd.DataFrame:
    datos = cargar_datos()
    return aplicar_filtros(
        df=datos,
        peajes=peajes,
        categorias=categorias,
        rango_fechas=rango_fechas,
        anios=anios,
        proporcion_registros=proporcion_registros,
    )
