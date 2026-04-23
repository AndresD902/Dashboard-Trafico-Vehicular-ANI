from __future__ import annotations

import pandas as pd
import streamlit as st

from datos.cargador import cargar_datos_filtrados
from procesamiento.metricas import (
    calcular_metricas_principales,
    resumen_categorias,
    serie_temporal,
    tarifas_categorias_comunes,
)
from visualizaciones.graficos import grafico_categorias, grafico_tarifas_categorias, grafico_tendencia
from visualizaciones.panel import (
    construir_filtros,
    inicializar_ultima_actualizacion,
    mostrar_encabezado,
    mostrar_insight_principal,
    mostrar_metricas,
)


def main() -> None:
    inicializar_ultima_actualizacion()
    try:
        datos_base = cargar_datos_filtrados([], [], None)
    except RuntimeError as error:
        st.error(str(error))
        return
    except ValueError as error:
        st.warning(str(error))
        return
    except Exception as error:
        st.error(f"Ocurrio un problema inesperado al cargar los datos: {error}")
        return

    if datos_base.empty:
        st.warning("La API no devolvio registros en este momento.")
        return

    mostrar_encabezado()
    peajes, categorias, rango_fechas, anios, proporcion_registros = construir_filtros(datos_base)
    datos = cargar_datos_filtrados(
        peajes=peajes,
        categorias=categorias,
        rango_fechas=(pd.Timestamp(rango_fechas[0]), pd.Timestamp(rango_fechas[1])),
        anios=anios,
        proporcion_registros=proporcion_registros,
    )

    if datos.empty:
        st.info("No hay datos para la combinacion de filtros seleccionada.")
        return

    st.caption(
        f"Registros entre {datos_base['desde'].min():%Y-%m-%d} y {datos_base['hasta'].max():%Y-%m-%d}"
    )

    mostrar_metricas(calcular_metricas_principales(datos))
    mostrar_insight_principal(datos)

    st.markdown('<div class="subtitulo-seccion">Resumen ejecutivo</div>', unsafe_allow_html=True)
    col_izquierda, col_derecha = st.columns([1.2, 1])
    with col_izquierda:
        st.plotly_chart(grafico_tendencia(serie_temporal(datos)), use_container_width=True)
        serie = serie_temporal(datos)
        if len(serie) >= 2:
            tendencia = "crecimiento" if serie.iloc[-1]["ingreso"] >= serie.iloc[-2]["ingreso"] else "caida"
            st.caption(
                f"Conclusion: se observa **{tendencia}** en el ultimo periodo analizado, con un ingreso estimado de "
                f"${serie.iloc[-1]['ingreso']:,.0f}.".replace(",", ".")
            )
        else:
            st.caption("Conclusion: aun no hay suficientes periodos para evaluar una tendencia temporal robusta.")
    with col_derecha:
        categorias_resumen = resumen_categorias(datos)
        st.plotly_chart(grafico_categorias(categorias_resumen), use_container_width=True)
        if not categorias_resumen.empty:
            st.caption(
                f"Conclusion: la categoria con mayor ingreso estimado fue **{categorias_resumen.iloc[0]['categoria_tarifa']}**."
            )

    st.markdown('<div class="subtitulo-seccion">Tarifas mas comunes</div>', unsafe_allow_html=True)
    tarifas_comunes = tarifas_categorias_comunes(datos)
    if not tarifas_comunes.empty:
        st.plotly_chart(grafico_tarifas_categorias(tarifas_comunes), use_container_width=True)
        st.caption(
            f"Conclusion: la categoria **{tarifas_comunes.iloc[0]['categoria_tarifa']}** es de las mas frecuentes y registra una tarifa promedio de "
            f"${tarifas_comunes.iloc[0]['tarifa_promedio']:,.0f}.".replace(",", ".")
        )


main()
