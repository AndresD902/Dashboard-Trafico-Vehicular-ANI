from __future__ import annotations

from datetime import datetime

import streamlit as st

from procesamiento.metricas import ranking_peajes, resumen_categorias


def formatear_numero(valor: float, moneda: bool = False) -> str:
    if moneda:
        return f"${valor:,.0f}".replace(",", ".")
    return f"{valor:,.0f}".replace(",", ".")


def mostrar_encabezado() -> None:
    ultima_actualizacion = st.session_state.get("ultima_actualizacion_texto", "No disponible")
    enlace_dataset = "https://www.datos.gov.co/Transporte/Tr-fico-Vehicular-ANI/8yi9-t44c/about_data"
    st.markdown(
        """
        <div class="bloque-hero">
            <h1 style="margin-bottom:0.35rem;">Dashboard de Peajes en Colombia</h1>
            <p style="margin:0; font-size:1rem;">
                Analisis dinamico del trafico, recaudo estimado, evasores y exenciones
                con datos publicos consumidos en tiempo real desde datos.gov.co.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_1, col_2, col_3 = st.columns([1.2, 1.2, 1])
    with col_1:
        st.caption("Objetivo: transformar datos publicos de peajes en decisiones de negocio claras.")
    with col_2:
        st.markdown(
            f'<p class="meta-encabezado"><a href="{enlace_dataset}" target="_blank">Fuente</a></p>',
            unsafe_allow_html=True,
        )
    with col_3:
        st.caption(f"Ultima actualizacion: {ultima_actualizacion}")


def mostrar_tarjeta_metrica(titulo: str, valor: str, ayuda: str) -> None:
    st.markdown(
        f"""
        <div class="tarjeta-metrica">
            <div class="tarjeta-metrica-titulo">{titulo}</div>
            <div class="tarjeta-metrica-valor">{valor}</div>
            <div class="tarjeta-metrica-ayuda">{ayuda}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_metricas(metricas: dict[str, float]) -> None:
    columnas = st.columns(4)
    definiciones = [
        ("Total general", formatear_numero(metricas["total_general"], moneda=True), "Suma del ingreso estimado"),
        ("Promedio", formatear_numero(metricas["promedio_general"], moneda=True), "Promedio por registro filtrado"),
        ("Valor maximo", formatear_numero(metricas["valor_maximo"], moneda=True), "Mayor ingreso estimado observado"),
        ("Variacion", f"{metricas['variacion_porcentual']:.1f}%", "Cambio vs. el periodo anterior"),
    ]

    for columna, (titulo, valor, ayuda) in zip(columnas, definiciones):
        with columna:
            mostrar_tarjeta_metrica(titulo, valor, ayuda)


def mostrar_tarjeta_pregunta(numero: int, pregunta: str, respuesta: str) -> None:
    st.markdown(
        f"""
        <div class="tarjeta-pregunta">
            <div class="etiqueta-pregunta">Pregunta {numero}</div>
            <div class="titulo-pregunta">{pregunta}</div>
            <div class="respuesta-pregunta">{respuesta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_preguntas_desplegables(preguntas: list[dict[str, str]]) -> None:
    st.markdown('<div class="subtitulo-seccion">Preguntas del analisis</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="bloque-contexto">
            Abre cada pregunta para ver que busca responder el dashboard antes de revisar los graficos.
        </div>
        """,
        unsafe_allow_html=True,
    )
    for item in preguntas:
        with st.expander(f"Pregunta {item['numero']}: {item['pregunta']}"):
            st.write(item["descripcion"])


def abrir_bloque_pregunta(numero: int, pregunta: str) -> None:
    st.markdown(
        f"""
        <div class="cabecera-pregunta-panel">
            <div class="cabecera-pregunta">
                <div class="insignia-pregunta">P{numero}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cerrar_bloque_pregunta(hallazgo: str, conclusion: str) -> None:
    st.markdown(
        f"""
        <div class="bloque-hallazgo">
            <div class="titulo-hallazgo">Hallazgo importante</div>
            <div class="texto-hallazgo">{hallazgo}</div>
        </div>
        <div class="bloque-conclusion">
            <div class="titulo-hallazgo">Conclusion</div>
            <div class="texto-hallazgo">{conclusion}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_insight_principal(df) -> None:
    peaje_lider = ranking_peajes(df, limite=1)
    categoria_lider = resumen_categorias(df).head(1)

    if not peaje_lider.empty and not categoria_lider.empty:
        st.info(
            "Insight destacado: "
            f"**{peaje_lider.iloc[0]['peaje']}** lidera el trafico acumulado, mientras que la "
            f"categoria **{categoria_lider.iloc[0]['categoria_tarifa']}** concentra el mayor ingreso estimado."
        )


def construir_filtros(df):
    st.sidebar.title("Filtros")
    st.sidebar.caption("Ajusta el analisis para responder preguntas de negocio.")

    peajes = sorted(df["peaje"].dropna().unique().tolist())
    categorias = sorted(df["categoria_tarifa"].dropna().unique().tolist())
    anios_disponibles = sorted(df["anio"].dropna().unique().tolist())
    fecha_minima = df["hasta"].min().date()
    fecha_maxima = df["hasta"].max().date()

    anios_seleccionados = st.sidebar.multiselect(
        "Años",
        options=anios_disponibles,
        default=anios_disponibles,
        help="Selecciona uno o varios anios para recargar todo el dashboard con ese periodo.",
    )

    peajes_seleccionados = st.sidebar.multiselect(
        "Peajes",
        options=peajes,
        default=[],
        placeholder="Selecciona uno o varios peajes",
    )
    categorias_seleccionadas = st.sidebar.multiselect(
        "Categorias tarifarias",
        options=categorias,
        default=categorias,
    )
    tipo_selector = st.sidebar.selectbox(
        "Tipo de analisis",
        options=["Todos", "Categorias altas", "Categorias bajas"],
        index=0,
    )
    porcentaje_registros = st.sidebar.slider(
        "Porcentaje de registros",
        min_value=0,
        max_value=100,
        value=100,
        step=1,
        help="Permite reducir la muestra del dashboard a un porcentaje de los registros filtrados.",
    )
    rango = st.sidebar.date_input(
        "Rango de fechas",
        value=(fecha_minima, fecha_maxima),
        min_value=fecha_minima,
        max_value=fecha_maxima,
    )
    if st.sidebar.button("Recargar datos", use_container_width=True):
        st.cache_data.clear()
        st.session_state["ultima_actualizacion_texto"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

    if len(rango) == 2:
        rango_fechas = rango
    else:
        rango_fechas = (fecha_minima, fecha_maxima)

    if tipo_selector == "Categorias altas":
        categorias_seleccionadas = [categoria for categoria in categorias_seleccionadas if categoria in {"IV", "V", "VI", "VII"}]
    elif tipo_selector == "Categorias bajas":
        categorias_seleccionadas = [categoria for categoria in categorias_seleccionadas if categoria in {"I", "II", "III"}]

    return (
        peajes_seleccionados,
        categorias_seleccionadas,
        rango_fechas,
        anios_seleccionados,
        porcentaje_registros / 100,
    )


def inicializar_ultima_actualizacion() -> None:
    if "ultima_actualizacion_texto" not in st.session_state:
        st.session_state["ultima_actualizacion_texto"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
