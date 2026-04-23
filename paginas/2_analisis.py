from __future__ import annotations

import pandas as pd
import streamlit as st

from datos.cargador import cargar_datos_filtrados
from procesamiento.metricas import (
    categoria_mayor_ingreso,
    concentracion_top_5,
    correlacion_trafico_ingreso,
    mes_mayor_ingreso,
    peaje_mayor_evasion,
    ranking_peajes,
    ranking_evasion,
    relacion_trafico_ingreso,
    resumen_categorias,
    serie_temporal,
    tarifas_categorias_comunes,
    top_peaje_por_ingreso,
)
from visualizaciones.graficos import (
    grafico_categorias,
    grafico_evasion,
    grafico_relacion_trafico_ingreso,
    grafico_ranking,
    grafico_ranking_ingreso,
    grafico_tarifas_categorias,
    grafico_tendencia_ingreso,
)
from visualizaciones.panel import (
    abrir_bloque_pregunta,
    cerrar_bloque_pregunta,
    construir_filtros,
    inicializar_ultima_actualizacion,
    mostrar_preguntas_desplegables,
)


def main() -> None:
    inicializar_ultima_actualizacion()
    st.markdown('<div class="subtitulo-seccion">Analisis comparativo</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="bloque-contexto">
            Esta seccion responde preguntas de negocio concretas sobre concentracion de ingresos,
            comportamiento temporal, evasion y relacion entre trafico y recaudo.
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    preguntas = [
        {
            "numero": "1",
            "pregunta": "Que peaje genera mas ingreso estimado?",
            "descripcion": "Identifica el peaje lider en recaudo estimado para detectar el punto mas relevante del sistema dentro de los filtros activos.",
        },
        {
            "numero": "2",
            "pregunta": "Que categoria aporta mas recaudo?",
            "descripcion": "Compara categorias tarifarias para ver cual concentra mas ingreso y tiene mayor peso en el comportamiento financiero.",
        },
        {
            "numero": "3",
            "pregunta": "En que momento del tiempo se observo el pico de ingreso?",
            "descripcion": "Busca el punto mas alto de la serie temporal para reconocer meses especialmente fuertes dentro del periodo analizado.",
        },
        {
            "numero": "4",
            "pregunta": "Que tarifas dominan en las categorias mas comunes?",
            "descripcion": "Cruza frecuencia y tarifa promedio para encontrar categorias que aparecen mucho y ademas tienen impacto economico constante.",
        },
        {
            "numero": "5",
            "pregunta": "Que peaje requiere mayor atencion por evasion?",
            "descripcion": "Ordena los peajes por tasa de evasion para ubicar donde podria haber mayor riesgo operativo o de control.",
        },
        {
            "numero": "6",
            "pregunta": "Existe relacion entre trafico e ingreso?",
            "descripcion": "Evalua si un mayor volumen vehicular suele venir acompanado de un mayor ingreso estimado entre los peajes comparados.",
        },
    ]

    mostrar_preguntas_desplegables(preguntas)

    peaje_ingreso = top_peaje_por_ingreso(datos)
    categoria_top = categoria_mayor_ingreso(datos)
    mejor_mes = mes_mayor_ingreso(datos)
    peaje_evasion = peaje_mayor_evasion(datos)
    share_top_5 = concentracion_top_5(datos)
    correlacion = correlacion_trafico_ingreso(datos)
    ranking_ingreso = (
        datos.groupby("peaje", as_index=False)
        .agg(ingreso=("ingreso_estimado", "sum"), trafico=("cantidadtrafico", "sum"))
        .sort_values("ingreso", ascending=False)
        .head(10)
    )
    categorias_resumen = resumen_categorias(datos)
    serie_ingresos = serie_temporal(datos)
    evasion_ranking = ranking_evasion(datos)
    relacion = relacion_trafico_ingreso(datos)
    tarifas_comunes = tarifas_categorias_comunes(datos)

    st.markdown('<div class="subtitulo-seccion">Respuestas visuales</div>', unsafe_allow_html=True)

    abrir_bloque_pregunta(1, "Que peaje genera mas ingreso estimado?")
    st.plotly_chart(grafico_ranking_ingreso(ranking_ingreso), use_container_width=True)
    cerrar_bloque_pregunta(
        hallazgo=(
            f"El peaje <strong>{peaje_ingreso.get('peaje', 'No disponible')}</strong> lidera el ingreso estimado con "
            f"<strong>${peaje_ingreso.get('ingreso', 0):,.0f}</strong>.".replace(",", ".")
        ),
        conclusion=(
            "Este peaje es una referencia clave para entender el comportamiento del recaudo y puede servir como punto de control "
            "para decisiones operativas y comparativas."
        ),
    )

    abrir_bloque_pregunta(2, "Que categoria aporta mas recaudo?")
    st.plotly_chart(grafico_categorias(categorias_resumen), use_container_width=True)
    cerrar_bloque_pregunta(
        hallazgo=(
            f"La categoria <strong>{categoria_top.get('categoria_tarifa', 'No disponible')}</strong> concentra el mayor ingreso "
            "estimado dentro del rango seleccionado."
        ),
        conclusion=(
            "La mezcla tarifaria no aporta por igual al sistema; conviene priorizar el seguimiento de la categoria dominante "
            "porque tiene mayor impacto sobre el resultado financiero."
        ),
    )

    abrir_bloque_pregunta(3, "En que momento del tiempo se observo el pico de ingreso?")
    st.plotly_chart(grafico_tendencia_ingreso(serie_ingresos), use_container_width=True)
    mes_pico = (
        pd.Timestamp(mejor_mes.get("periodo")).strftime("%Y-%m")
        if "periodo" in mejor_mes else "No disponible"
    )
    cerrar_bloque_pregunta(
        hallazgo=(
            f"El periodo con mayor ingreso estimado fue <strong>{mes_pico}</strong>, lo que marca el punto mas alto de la serie temporal."
        ),
        conclusion=(
            "Identificar el mes pico ayuda a reconocer estacionalidad o eventos excepcionales y sirve como base para contrastar periodos "
            "de bajo rendimiento."
        ),
    )

    abrir_bloque_pregunta(4, "Que tarifas dominan en las categorias mas comunes?")
    st.plotly_chart(grafico_tarifas_categorias(tarifas_comunes), use_container_width=True)
    if not tarifas_comunes.empty:
        cerrar_bloque_pregunta(
            hallazgo=(
                f"La categoria <strong>{tarifas_comunes.iloc[0]['categoria_tarifa']}</strong> aparece entre las mas frecuentes y presenta una "
                f"tarifa promedio cercana a <strong>${tarifas_comunes.iloc[0]['tarifa_promedio']:,.0f}</strong>.".replace(",", ".")
            ),
            conclusion=(
                "Este cruce entre frecuencia y tarifa ayuda a detectar que categorias combinan presencia alta con impacto economico sostenido "
                "dentro del dashboard."
            ),
        )
    else:
        st.info("No hay datos suficientes para resumir las tarifas de las categorias mas comunes.")
        cerrar_bloque_pregunta(
            hallazgo="No fue posible calcular una tarifa representativa para las categorias seleccionadas.",
            conclusion="Conviene ampliar los filtros o aumentar el porcentaje de registros para enriquecer este analisis.",
        )

    abrir_bloque_pregunta(5, "Que peaje requiere mayor atencion por evasion?")
    st.plotly_chart(grafico_evasion(evasion_ranking), use_container_width=True)
    cerrar_bloque_pregunta(
        hallazgo=(
            f"El peaje <strong>{peaje_evasion.get('peaje', 'No disponible')}</strong> presenta la mayor tasa de evasion relativa "
            "entre los peajes analizados."
        ),
        conclusion=(
            "Este resultado sugiere una oportunidad clara para reforzar control, monitoreo y acciones de mitigacion donde el impacto "
            "operativo puede ser mas alto."
        ),
    )

    abrir_bloque_pregunta(6, "Existe relacion entre trafico e ingreso?")
    st.plotly_chart(grafico_relacion_trafico_ingreso(relacion), use_container_width=True)
    intensidad = "alta" if correlacion >= 0.7 else "moderada" if correlacion >= 0.4 else "baja"
    cerrar_bloque_pregunta(
        hallazgo=(
            f"La correlacion estimada entre trafico e ingreso es <strong>{correlacion:.2f}</strong>, lo que indica una relacion "
            f"<strong>{intensidad}</strong>."
        ),
        conclusion=(
            "La linea de tendencia ayuda a ver si los peajes con mayor trafico tambien elevan el ingreso de forma consistente. "
            "Asi la relacion se interpreta mejor que en un grafico con demasiadas variables a la vez."
        ),
    )

    st.markdown(
        f"""
        <div class="bloque-contexto">
            Insight ejecutivo: los 5 peajes con mayor desempeno concentran aproximadamente <strong>{share_top_5:.1f}%</strong>
            del ingreso estimado del filtro actual, lo que ayuda a dimensionar el grado de concentracion del sistema.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="subtitulo-seccion">Lectura complementaria</div>', unsafe_allow_html=True)
    st.plotly_chart(grafico_ranking(ranking_peajes(datos)), use_container_width=True)
    st.caption(
        "Conclusion adicional: el ranking por trafico complementa el de ingreso y ayuda a distinguir volumen alto de recaudo alto."
    )


main()
