from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

COLORES = {
    "primario": "#5f7c6c",
    "secundario": "#7b8f7a",
    "acento": "#c4865a",
    "fondo": "#eef2ea",
    "fondo_panel": "#f6f3eb",
    "texto": "#203229",
    "texto_suave": "#5b6b63",
    "borde": "rgba(95, 124, 108, 0.18)",
}


@dataclass(frozen=True)
class ConfiguracionAPI:
    url_base: str
    token_app: str | None
    limite_por_peticion: int
    tiempo_espera: int = 30


def obtener_configuracion() -> ConfiguracionAPI:
    return ConfiguracionAPI(
        url_base=os.getenv(
            "API_PEAJES_URL",
            "https://www.datos.gov.co/resource/8yi9-t44c.json",
        ),
        token_app=os.getenv("SOCRATA_APP_TOKEN") or None,
        limite_por_peticion=int(os.getenv("LIMITE_API", "50000")),
    )


def aplicar_estilos_generales() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --color-primario: {COLORES["primario"]};
                --color-secundario: {COLORES["secundario"]};
                --color-acento: {COLORES["acento"]};
                --color-fondo: {COLORES["fondo"]};
                --color-panel: {COLORES["fondo_panel"]};
                --color-texto: {COLORES["texto"]};
                --color-texto-suave: {COLORES["texto_suave"]};
                --color-borde: {COLORES["borde"]};
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top right, rgba(196, 134, 90, 0.18), transparent 24%),
                    radial-gradient(circle at top left, rgba(95, 124, 108, 0.14), transparent 26%),
                    linear-gradient(180deg, #f7f5ef 0%, {COLORES["fondo"]} 100%);
                color: var(--color-texto);
            }}

            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}

            div[data-testid="stSpinner"] {{
                margin-top: 3.25rem;
                position: relative;
                z-index: 2;
            }}

            .bloque-hero {{
                padding: 2rem 2.2rem;
                border-radius: 28px;
                background:
                    linear-gradient(135deg, rgba(96, 123, 109, 0.95) 0%, rgba(123, 143, 122, 0.92) 56%, rgba(196, 134, 90, 0.82) 100%);
                color: #fcfbf7;
                box-shadow: 0 24px 60px rgba(54, 68, 58, 0.18);
                margin-bottom: 1.35rem;
                border: 1px solid rgba(255, 255, 255, 0.18);
            }}

            .tarjeta-metrica {{
                background: rgba(246, 243, 235, 0.82);
                border: 1px solid var(--color-borde);
                border-radius: 22px;
                padding: 1.1rem 1rem;
                box-shadow: 0 14px 36px rgba(48, 60, 52, 0.08);
                backdrop-filter: blur(6px);
                text-align: center;
            }}

            .tarjeta-metrica-titulo {{
                font-size: 0.9rem;
                color: #475569;
                text-align: center;
            }}

            .tarjeta-metrica-valor {{
                font-size: 1.7rem;
                font-weight: 700;
                color: #0f172a;
                text-align: center;
            }}

            .tarjeta-metrica-ayuda {{
                font-size: 0.82rem;
                color: #64748b;
                text-align: center;
            }}

            .subtitulo-seccion {{
                margin-top: 0.4rem;
                margin-bottom: 1rem;
                color: var(--color-secundario);
                font-weight: 700;
                font-size: 1.15rem;
                letter-spacing: 0.02em;
            }}

            .meta-encabezado {{
                margin: 0;
                color: rgb(91, 107, 99);
                font-size: 0.875rem;
            }}

            .meta-encabezado a {{
                color: inherit;
                text-decoration: none;
            }}

            .meta-encabezado a:hover {{
                text-decoration: underline;
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #f2f0e7 0%, #dde7dd 100%);
                border-right: 1px solid var(--color-borde);
            }}

            /* ===== MÉTRICAS ===== */
            [data-testid="stMetric"],
            div[data-testid="stExpander"] {{
                background: rgba(246, 243, 235, 0.72);
                border: 1px solid var(--color-borde);
                border-radius: 18px;
            }}

            [data-testid="stMetric"] {{
                padding: 0.9rem 0.75rem;
                min-height: 110px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center !important;
            }}

            [data-testid="stMetric"] > div {{
                width: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
            }}

            [data-testid="stMetricLabel"] {{
                width: 100%;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                margin-bottom: 0.35rem;
                text-align: center !important;
            }}

            [data-testid="stMetricLabel"] > div {{
                width: 100%;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
            }}

            [data-testid="stMetricLabel"] p {{
                width: 100%;
                margin: 0 !important;
                text-align: center !important;
                font-size: 0.95rem;
                line-height: 1.25;
            }}

            [data-testid="stMetricValue"] {{
                width: 100%;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
            }}

            [data-testid="stMetricValue"] > div {{
                width: 100%;
                text-align: center !important;
                justify-content: center !important;
            }}

            [data-testid="stMetricValue"] p {{
                width: 100%;
                margin: 0 !important;
                text-align: center !important;
            }}

            [data-testid="stMetricDelta"] {{
                width: 100%;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
            }}

            /* Fuerza final por si Streamlit cambia el DOM */
            [data-testid="stMetric"] *,
            [data-testid="stMetricLabel"] *,
            [data-testid="stMetricValue"] * {{
                text-align: center !important;
            }}

            div[data-testid="stPlotlyChart"] {{
                background: rgba(246, 243, 235, 0.68);
                border: 1px solid var(--color-borde);
                border-radius: 22px;
                padding: 0.4rem 0.6rem 0.2rem 0.6rem;
                box-shadow: 0 12px 30px rgba(48, 60, 52, 0.07);
            }}

            .tarjeta-pregunta {{
                background: rgba(246, 243, 235, 0.82);
                border: 1px solid var(--color-borde);
                border-radius: 22px;
                padding: 1rem 1.1rem;
                min-height: 172px;
                box-shadow: 0 14px 32px rgba(48, 60, 52, 0.07);
            }}

            .etiqueta-pregunta {{
                display: inline-block;
                padding: 0.28rem 0.58rem;
                border-radius: 999px;
                background: rgba(95, 124, 108, 0.14);
                color: var(--color-primario);
                font-size: 0.78rem;
                font-weight: 700;
                margin-bottom: 0.7rem;
            }}

            .titulo-pregunta {{
                color: var(--color-texto);
                font-size: 1.02rem;
                font-weight: 700;
                margin-bottom: 0.45rem;
                line-height: 1.35;
            }}

            .respuesta-pregunta {{
                color: var(--color-texto-suave);
                font-size: 0.93rem;
                line-height: 1.55;
            }}

            .bloque-contexto {{
                background: rgba(246, 243, 235, 0.66);
                border: 1px solid var(--color-borde);
                border-radius: 20px;
                padding: 1rem 1.1rem;
                margin-bottom: 1rem;
            }}

            .cabecera-pregunta-panel {{
                background: linear-gradient(180deg, rgba(248, 246, 239, 0.92) 0%, rgba(241, 239, 231, 0.86) 100%);
                border: 1px solid var(--color-borde);
                border-radius: 999px;
                padding: 0.35rem 0.55rem;
                margin-bottom: 0.7rem;
                box-shadow: 0 8px 18px rgba(48, 60, 52, 0.05);
                width: fit-content;
            }}

            .cabecera-pregunta {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0;
                margin-bottom: 0;
            }}

            .insignia-pregunta {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: rgba(95, 124, 108, 0.14);
                color: var(--color-primario);
                width: 1.8rem;
                height: 1.8rem;
                min-width: 1.8rem;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 700;
                line-height: 1;
                box-shadow: inset 0 0 0 1px rgba(95, 124, 108, 0.08);
            }}

            .bloque-hallazgo, .bloque-conclusion {{
                background: rgba(255, 255, 255, 0.44);
                border: 1px solid var(--color-borde);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                margin-top: 0.7rem;
            }}

            .titulo-hallazgo {{
                color: var(--color-secundario);
                font-size: 0.8rem;
                font-weight: 800;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
            }}

            .texto-hallazgo {{
                color: var(--color-texto-suave);
                font-size: 0.95rem;
                line-height: 1.55;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )