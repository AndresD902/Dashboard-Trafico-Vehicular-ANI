from __future__ import annotations

import streamlit as st

from utilidades.configuracion import aplicar_estilos_generales


def main() -> None:
    st.set_page_config(
        page_title="Proyecto Streamlit API",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    aplicar_estilos_generales()

    navegacion = st.navigation(
        [
            st.Page("paginas/1_resumen.py", title="Resumen", icon=":material/dashboard:"),
            st.Page("paginas/2_analisis.py", title="Analisis", icon=":material/monitoring:"),
            st.Page("paginas/3_datos.py", title="Datos", icon=":material/table_view:"),
        ]
    )

    navegacion.run()


main()
