from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utilidades.configuracion import COLORES


def _aplicar_estilo_figura(figura):
    figura.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.12)",
        font={"color": COLORES["texto"], "family": "Trebuchet MS, Segoe UI, sans-serif"},
        title={"x": 0.03, "font": {"size": 20}},
        margin={"l": 24, "r": 24, "t": 64, "b": 24},
    )
    figura.update_xaxes(showgrid=False, zeroline=False)
    figura.update_yaxes(gridcolor="rgba(95, 124, 108, 0.12)", zeroline=False)
    return figura


def grafico_tendencia(df: pd.DataFrame):
    figura = make_subplots(specs=[[{"secondary_y": True}]])
    figura.add_trace(
        go.Scatter(
            x=df["periodo"],
            y=df["trafico"],
            mode="lines+markers",
            name="trafico",
            line={"color": COLORES["primario"], "width": 3},
            marker={"size": 6},
        ),
        secondary_y=False,
    )
    figura.add_trace(
        go.Scatter(
            x=df["periodo"],
            y=df["ingreso"],
            mode="lines+markers",
            name="ingreso",
            line={"color": COLORES["acento"], "width": 3},
            marker={"size": 6},
        ),
        secondary_y=True,
    )
    figura.update_layout(
        title="Evolucion mensual de trafico e ingreso estimado",
        hovermode="x unified",
        legend_title_text="Serie",
    )
    figura.update_xaxes(title_text="Periodo", showgrid=False, zeroline=False)
    figura.update_yaxes(title_text="Trafico", secondary_y=False, gridcolor="rgba(95, 124, 108, 0.12)")
    figura.update_yaxes(title_text="Ingreso estimado", secondary_y=True, showgrid=False)
    return _aplicar_estilo_figura(figura)


def grafico_ranking(df: pd.DataFrame):
    figura = px.bar(
        df.sort_values("trafico"),
        x="trafico",
        y="peaje",
        orientation="h",
        title="Top 10 peajes con mayor trafico",
        labels={"trafico": "Trafico acumulado", "peaje": "Peaje"},
        color="ingreso",
        color_continuous_scale="Tealgrn",
    )
    figura.update_layout(coloraxis_colorbar_title="Ingreso")
    return _aplicar_estilo_figura(figura)


def grafico_ranking_ingreso(df: pd.DataFrame):
    figura = px.bar(
        df.sort_values("ingreso"),
        x="ingreso",
        y="peaje",
        orientation="h",
        title="Ranking de peajes por ingreso estimado",
        labels={"ingreso": "Ingreso estimado", "peaje": "Peaje"},
        color="trafico",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    return _aplicar_estilo_figura(figura)


def grafico_categorias(df: pd.DataFrame):
    figura = px.bar(
        df,
        x="categoria_tarifa",
        y="ingreso",
        title="Ingreso estimado por categoria tarifaria",
        labels={"categoria_tarifa": "Categoria", "ingreso": "Ingreso estimado"},
        color="trafico",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    return _aplicar_estilo_figura(figura)


def grafico_tendencia_ingreso(df: pd.DataFrame):
    figura = px.line(
        df,
        x="periodo",
        y="ingreso",
        markers=True,
        title="Evolucion del ingreso estimado por periodo",
        labels={"periodo": "Periodo", "ingreso": "Ingreso estimado"},
        color_discrete_sequence=[COLORES["primario"]],
    )
    figura.update_traces(line={"width": 4})
    return _aplicar_estilo_figura(figura)


def grafico_crecimiento(df: pd.DataFrame):
    figura = px.bar(
        df,
        x="periodo",
        y="variacion_porcentual",
        title="Variacion porcentual del ingreso entre periodos",
        labels={"periodo": "Periodo", "variacion_porcentual": "Variacion %"},
        color="variacion_porcentual",
        color_continuous_scale=[
            [0.0, "#b75d4b"],
            [0.5, "#d8d4c8"],
            [1.0, COLORES["primario"]],
        ],
    )
    return _aplicar_estilo_figura(figura)


def grafico_dispersion(df: pd.DataFrame):
    figura = px.scatter(
        df,
        x="trafico",
        y="ingreso",
        size="evasores",
        color="exentos",
        hover_name="peaje",
        title="Relacion entre trafico, ingreso, evasores y exentos",
        labels={
            "trafico": "Trafico acumulado",
            "ingreso": "Ingreso estimado",
            "evasores": "Evasores",
            "exentos": "Exentos",
        },
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["primario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    figura.update_layout(coloraxis_colorbar_title="Exentos")
    return _aplicar_estilo_figura(figura)


def grafico_relacion_trafico_ingreso(df: pd.DataFrame):
    figura = go.Figure()
    figura.add_trace(
        go.Scatter(
            x=df["trafico"],
            y=df["ingreso"],
            mode="markers+text",
            text=df["peaje"],
            textposition="top center",
            textfont={"size": 10},
            marker={
                "size": 11,
                "color": COLORES["primario"],
                "line": {"color": COLORES["secundario"], "width": 1},
                "opacity": 0.78,
            },
            name="Peajes",
            hovertemplate="Peaje: %{text}<br>Trafico: %{x:,.0f}<br>Ingreso: %{y:,.0f}<extra></extra>",
        )
    )
    figura.add_trace(
        go.Scatter(
            x=df["trafico"],
            y=df["ingreso_ajustado"],
            mode="lines",
            line={"color": COLORES["acento"], "width": 3, "dash": "dash"},
            name="Tendencia",
            hoverinfo="skip",
        )
    )
    figura.update_layout(
        title="Relacion entre trafico e ingreso por peaje",
        xaxis_title="Trafico acumulado",
        yaxis_title="Ingreso estimado",
        legend_title_text="Serie",
    )
    return _aplicar_estilo_figura(figura)


def grafico_evasion(df: pd.DataFrame):
    figura = px.bar(
        df.sort_values("tasa_evasion"),
        x="tasa_evasion",
        y="peaje",
        orientation="h",
        title="Peajes con mayor tasa de evasion",
        labels={"tasa_evasion": "Tasa de evasion", "peaje": "Peaje"},
        color="evasores",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, "#b75d4b"],
        ],
    )
    figura.update_layout(coloraxis_colorbar_title="Evasores")
    return _aplicar_estilo_figura(figura)


def grafico_tarifas_categorias(df: pd.DataFrame):
    figura = px.bar(
        df.sort_values("frecuencia"),
        x="tarifa_promedio",
        y="categoria_tarifa",
        orientation="h",
        title="Tarifas promedio de las categorias mas comunes",
        labels={"tarifa_promedio": "Tarifa promedio", "categoria_tarifa": "Categoria"},
        color="frecuencia",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    figura.update_layout(coloraxis_colorbar_title="Frecuencia")
    return _aplicar_estilo_figura(figura)


def grafico_frecuencia_categorias(df: pd.DataFrame):
    figura = px.bar(
        df.sort_values("registros"),
        x="registros",
        y="categoria_tarifa",
        orientation="h",
        title="Categorias con mayor numero de registros",
        labels={"registros": "Cantidad de registros", "categoria_tarifa": "Categoria"},
        color="ingreso",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    figura.update_layout(coloraxis_colorbar_title="Ingreso")
    return _aplicar_estilo_figura(figura)


def grafico_registros_anuales(df: pd.DataFrame):
    figura = px.bar(
        df,
        x="anio",
        y="registros",
        title="Cobertura de registros por años",
        labels={"anio": "Anio", "registros": "Cantidad de registros"},
        color="ingreso",
        color_continuous_scale=[
            [0.0, "#dfe8db"],
            [0.5, COLORES["secundario"]],
            [1.0, COLORES["acento"]],
        ],
    )
    figura.update_layout(coloraxis_colorbar_title="Ingreso")
    return _aplicar_estilo_figura(figura)
