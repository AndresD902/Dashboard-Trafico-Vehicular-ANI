from __future__ import annotations

import numpy as np
import pandas as pd


def calcular_metricas_principales(df: pd.DataFrame) -> dict[str, float]:
    if df.empty:
        return {
            "total_general": 0,
            "promedio_general": 0,
            "valor_maximo": 0,
            "variacion_porcentual": 0,
        }

    serie_ingresos = serie_temporal(df)
    variacion_porcentual = 0.0
    if len(serie_ingresos) >= 2 and serie_ingresos.iloc[-2]["ingreso"] != 0:
        variacion_porcentual = (
            (serie_ingresos.iloc[-1]["ingreso"] - serie_ingresos.iloc[-2]["ingreso"])
            / serie_ingresos.iloc[-2]["ingreso"]
        ) * 100

    return {
        "total_general": float(df["ingreso_estimado"].sum()),
        "promedio_general": float(df["ingreso_estimado"].mean()),
        "valor_maximo": float(df["ingreso_estimado"].max()),
        "variacion_porcentual": float(variacion_porcentual),
    }


def serie_temporal(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["periodo", "trafico", "ingreso", "evasores"])

    return (
        df.groupby("periodo", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
            evasores=("cantidadevasores", "sum"),
        )
        .sort_values("periodo")
    )


def ranking_peajes(df: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["peaje", "trafico", "ingreso", "evasores"])

    return (
        df.groupby("peaje", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
            evasores=("cantidadevasores", "sum"),
        )
        .sort_values("trafico", ascending=False)
        .head(limite)
    )


def resumen_categorias(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["categoria_tarifa", "trafico", "ingreso", "tarifa_promedio"])

    return (
        df.groupby("categoria_tarifa", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
            tarifa_promedio=("valortarifa", "mean"),
        )
        .sort_values("trafico", ascending=False)
    )


def dispersion_peajes(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["peaje", "trafico", "ingreso", "evasores", "exentos"])

    return (
        df.groupby("peaje", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
            evasores=("cantidadevasores", "sum"),
            exentos=("cantidadexentos787", "sum"),
        )
        .sort_values("ingreso", ascending=False)
    )


def matriz_calor_categoria_mes(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    tabla = (
        df.pivot_table(
            index="categoria_tarifa",
            columns="mes",
            values="ingreso_estimado",
            aggfunc="sum",
            fill_value=0,
        )
        .sort_index()
    )
    return tabla


def top_peaje_por_ingreso(df: pd.DataFrame) -> pd.Series:
    ranking = (
        df.groupby("peaje", as_index=False)
        .agg(
            ingreso=("ingreso_estimado", "sum"),
            trafico=("cantidadtrafico", "sum"),
            evasores=("cantidadevasores", "sum"),
        )
        .sort_values("ingreso", ascending=False)
    )
    return ranking.iloc[0] if not ranking.empty else pd.Series(dtype="object")


def categoria_mayor_ingreso(df: pd.DataFrame) -> pd.Series:
    categorias = resumen_categorias(df).sort_values("ingreso", ascending=False)
    return categorias.iloc[0] if not categorias.empty else pd.Series(dtype="object")


def mes_mayor_ingreso(df: pd.DataFrame) -> pd.Series:
    serie = serie_temporal(df).sort_values("ingreso", ascending=False)
    return serie.iloc[0] if not serie.empty else pd.Series(dtype="object")


def mes_mayor_crecimiento(df: pd.DataFrame) -> pd.Series:
    serie = serie_temporal(df).copy()
    if serie.empty:
        return pd.Series(dtype="object")
    serie["variacion_porcentual"] = serie["ingreso"].pct_change() * 100
    serie = serie.dropna(subset=["variacion_porcentual"]).sort_values("variacion_porcentual", ascending=False)
    return serie.iloc[0] if not serie.empty else pd.Series(dtype="object")


def peaje_mayor_evasion(df: pd.DataFrame) -> pd.Series:
    peajes = (
        df.groupby("peaje", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            evasores=("cantidadevasores", "sum"),
        )
    )
    if peajes.empty:
        return pd.Series(dtype="object")
    peajes = peajes[peajes["trafico"] > 0].copy()
    peajes["tasa_evasion"] = peajes["evasores"] / peajes["trafico"]
    peajes = peajes.sort_values(["tasa_evasion", "evasores"], ascending=False)
    return peajes.iloc[0] if not peajes.empty else pd.Series(dtype="object")


def concentracion_top_5(df: pd.DataFrame) -> float:
    ranking = ranking_peajes(df, limite=5)
    total = float(df["ingreso_estimado"].sum())
    if ranking.empty or total == 0:
        return 0.0
    return float(ranking["ingreso"].sum() / total * 100)


def correlacion_trafico_ingreso(df: pd.DataFrame) -> float:
    dispersion = dispersion_peajes(df)
    if dispersion.empty or dispersion["trafico"].nunique() < 2 or dispersion["ingreso"].nunique() < 2:
        return 0.0
    return float(dispersion["trafico"].corr(dispersion["ingreso"]))


def serie_crecimiento(df: pd.DataFrame) -> pd.DataFrame:
    serie = serie_temporal(df).copy()
    if serie.empty:
        return pd.DataFrame(columns=["periodo", "variacion_porcentual"])
    serie["variacion_porcentual"] = serie["ingreso"].pct_change() * 100
    return serie.dropna(subset=["variacion_porcentual"])


def ranking_evasion(df: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    peajes = (
        df.groupby("peaje", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            evasores=("cantidadevasores", "sum"),
            ingreso=("ingreso_estimado", "sum"),
        )
    )
    if peajes.empty:
        return pd.DataFrame(columns=["peaje", "trafico", "evasores", "ingreso", "tasa_evasion"])
    peajes = peajes[peajes["trafico"] > 0].copy()
    peajes["tasa_evasion"] = peajes["evasores"] / peajes["trafico"]
    return peajes.sort_values(["tasa_evasion", "evasores"], ascending=False).head(limite)


def tarifas_categorias_comunes(df: pd.DataFrame, limite: int = 5) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["categoria_tarifa", "frecuencia", "tarifa_promedio", "tarifa_maxima"])

    return (
        df.groupby("categoria_tarifa", as_index=False)
        .agg(
            frecuencia=("categoria_tarifa", "count"),
            tarifa_promedio=("valortarifa", "mean"),
            tarifa_maxima=("valortarifa", "max"),
            trafico=("cantidadtrafico", "sum"),
        )
        .sort_values(["frecuencia", "trafico"], ascending=False)
        .head(limite)
    )


def relacion_trafico_ingreso(df: pd.DataFrame, limite: int = 30) -> pd.DataFrame:
    base = (
        df.groupby("peaje", as_index=False)
        .agg(
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
        )
        .sort_values("ingreso", ascending=False)
        .head(limite)
    )
    if base.empty:
        return pd.DataFrame(columns=["peaje", "trafico", "ingreso", "ingreso_ajustado"])

    if base["trafico"].nunique() >= 2 and base["ingreso"].nunique() >= 2:
        pendiente, intercepto = np.polyfit(base["trafico"], base["ingreso"], 1)
        base["ingreso_ajustado"] = base["trafico"] * pendiente + intercepto
    else:
        base["ingreso_ajustado"] = base["ingreso"]

    return base


def frecuencia_categorias(df: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["categoria_tarifa", "registros", "trafico", "ingreso"])

    return (
        df.groupby("categoria_tarifa", as_index=False)
        .agg(
            registros=("categoria_tarifa", "count"),
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
        )
        .sort_values(["registros", "trafico"], ascending=False)
        .head(limite)
    )


def registros_por_anio(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["anio", "registros", "trafico", "ingreso"])

    return (
        df.groupby("anio", as_index=False)
        .agg(
            registros=("anio", "count"),
            trafico=("cantidadtrafico", "sum"),
            ingreso=("ingreso_estimado", "sum"),
        )
        .sort_values("anio")
    )
