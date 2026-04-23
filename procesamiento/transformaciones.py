from __future__ import annotations

import pandas as pd


def aplicar_filtros(
    df: pd.DataFrame,
    peajes: list[str],
    categorias: list[str],
    rango_fechas: tuple[pd.Timestamp, pd.Timestamp] | None,
    anios: list[int] | None = None,
    proporcion_registros: float = 1.0,
) -> pd.DataFrame:
    if df.empty:
        return df

    filtrado = df.copy()

    if anios:
        filtrado = filtrado[filtrado["anio"].isin(anios)]

    if peajes:
        filtrado = filtrado[filtrado["peaje"].isin(peajes)]

    if categorias:
        filtrado = filtrado[filtrado["categoria_tarifa"].isin(categorias)]

    if rango_fechas:
        fecha_inicio, fecha_fin = rango_fechas
        filtrado = filtrado[
            (filtrado["hasta"] >= pd.Timestamp(fecha_inicio))
            & (filtrado["hasta"] <= pd.Timestamp(fecha_fin))
        ]

    proporcion_registros = max(0.0, min(proporcion_registros, 1.0))
    if proporcion_registros == 0.0:
        return filtrado.iloc[0:0]

    if proporcion_registros < 1.0 and not filtrado.empty:
        cantidad = max(1, int(len(filtrado) * proporcion_registros))
        filtrado = filtrado.sort_values("hasta", ascending=False).head(cantidad)

    return filtrado


def obtener_opciones_filtro(df: pd.DataFrame) -> tuple[list[str], list[str], tuple]:
    peajes = sorted(df["peaje"].dropna().unique().tolist())
    categorias = sorted(df["categoria_tarifa"].dropna().unique().tolist())
    fecha_minima = df["hasta"].min().date()
    fecha_maxima = df["hasta"].max().date()
    return peajes, categorias, (fecha_minima, fecha_maxima)
