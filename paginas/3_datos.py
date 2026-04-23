from __future__ import annotations

import pandas as pd
import streamlit as st

from datos.cargador import cargar_datos_filtrados
from procesamiento.metricas import frecuencia_categorias, registros_por_anio
from visualizaciones.graficos import grafico_frecuencia_categorias, grafico_registros_anuales
from visualizaciones.panel import construir_filtros, inicializar_ultima_actualizacion


def main() -> None:
    inicializar_ultima_actualizacion()
    st.markdown('<div class="subtitulo-seccion">Explorador de datos</div>', unsafe_allow_html=True)
    st.write("Explora que tan amplia es la muestra filtrada, en que categorias se concentra y luego revisa el detalle fila por fila.")

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

    columnas_visibles = [
        "peaje",
        "categoria_tarifa",
        "desde",
        "hasta",
        "valortarifa",
        "cantidadtrafico",
        "cantidadevasores",
        "cantidadexentos787",
        "ingreso_estimado",
    ]

    resumen_categorias_df = frecuencia_categorias(datos)
    resumen_anual_df = registros_por_anio(datos)

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.metric("Registros visibles", f"{len(datos):,}".replace(",", "."))
    with col_2:
        st.metric("Peajes en muestra", f"{datos['peaje'].nunique():,}".replace(",", "."))
    with col_3:
        st.metric("Categorias en muestra", f"{datos['categoria_tarifa'].nunique():,}".replace(",", "."))
    with col_4:
        st.metric("Años cubiertos", f"{datos['anio'].nunique():,}".replace(",", "."))

    col_izquierda, col_derecha = st.columns([1.1, 1])
    with col_izquierda:
        if not resumen_categorias_df.empty:
            st.plotly_chart(grafico_frecuencia_categorias(resumen_categorias_df), use_container_width=True)
            st.caption(
                f"Lectura: la categoria **{resumen_categorias_df.iloc[0]['categoria_tarifa']}** es la que mas registros aporta dentro de la muestra actual."
            )
    with col_derecha:
        if not resumen_anual_df.empty:
            st.plotly_chart(grafico_registros_anuales(resumen_anual_df), use_container_width=True)
            st.caption(
                "Lectura: este grafico deja claro como se distribuyen los registros por años dentro de los filtros seleccionados."
            )

    st.markdown('<div class="subtitulo-seccion">Detalle de registros</div>', unsafe_allow_html=True)
    st.dataframe(
        datos[columnas_visibles].sort_values("hasta", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "Conclusion: primero entiendes la composicion de la muestra y despues usas la tabla para validar tarifas, trafico y registros particulares."
    )

    csv = datos[columnas_visibles].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar datos filtrados en CSV",
        data=csv,
        file_name="datos_filtrados_peajes.csv",
        mime="text/csv",
    )


main()
