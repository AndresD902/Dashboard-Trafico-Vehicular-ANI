# Dashboard de Peajes en Colombia

Aplicacion desarrollada en Streamlit para analizar datos publicos de trafico vehicular en peajes de Colombia. El proyecto consume informacion en tiempo real desde la API abierta de `datos.gov.co`, la transforma y la presenta en un tablero interactivo con metricas, filtros y visualizaciones orientadas al analisis de recaudo, evasion y comportamiento del trafico.

## Objetivo del proyecto

Construir un dashboard interactivo que permita explorar y analizar informacion de peajes en Colombia a partir de datos abiertos, facilitando la interpretacion de indicadores clave para la toma de decisiones.

## Fuente de datos

- API publica: `https://www.datos.gov.co/resource/8yi9-t44c.json`
- Portal de referencia: `https://www.datos.gov.co/Transporte/Tr-fico-Vehicular-ANI/8yi9-t44c/about_data`

## Funcionalidades principales

- Consulta automatica de datos desde la API publica.
- Limpieza y transformacion de registros para analisis.
- Calculo de ingreso estimado, tasa de evasion y porcentaje de exentos.
- Filtros dinamicos por anio, peaje, categoria tarifaria, fechas y proporcion de registros.
- Visualizacion de tendencias de trafico e ingreso.
- Ranking de peajes por trafico, ingreso y evasion.
- Exploracion detallada de registros en tabla.
- Descarga de datos filtrados en formato CSV desde la pagina de datos.

## Secciones del dashboard

### 1. Resumen

Presenta una vista ejecutiva del comportamiento general del sistema:

- metricas principales de ingreso estimado
- evolucion mensual de trafico e ingreso
- categorias con mayor participacion
- insight principal del periodo analizado

### 2. Analisis

Responde preguntas de negocio con apoyo visual:

- que peaje genera mas ingreso estimado
- que categoria aporta mas recaudo
- en que periodo se registra el mayor ingreso
- que tarifas dominan en las categorias mas comunes
- que peajes muestran mayor evasion
- que relacion existe entre trafico e ingreso

### 3. Datos

Permite explorar los registros filtrados en forma tabular y descargar la muestra visible en CSV.

## Estructura del proyecto

```text
StreamLit/
|-- app.py
|-- requirements.txt
|-- render.yaml
|-- datos/
|   |-- cliente_api.py
|   |-- cargador.py
|-- procesamiento/
|   |-- limpieza.py
|   |-- transformaciones.py
|   |-- metricas.py
|-- visualizaciones/
|   |-- graficos.py
|   |-- panel.py
|-- utilidades/
|   |-- configuracion.py
|-- paginas/
|   |-- 1_resumen.py
|   |-- 2_analisis.py
|   |-- 3_datos.py
```

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- Python Dotenv

## Requisitos

- Python 3.11 o superior
- Conexion a internet para consultar la API

## Instalacion y ejecucion local

1. Clonar o abrir este proyecto en el equipo local.
2. Instalar las dependencias:

```bash
python -m venv .venv 
.venv\Scripts\activate  
pip install -r requirements.txt
```

3. Configurar las variables de entorno en el archivo `.env`:

```env
API_PEAJES_URL=https://www.datos.gov.co/resource/8yi9-t44c.json
SOCRATA_APP_TOKEN=
LIMITE_API=50000
```

4. Ejecutar la aplicacion:

```bash
streamlit run app.py
```

## Despliegue

El proyecto incluye el archivo `render.yaml`, por lo que puede desplegarse facilmente en Render. Si se desea mayor estabilidad frente a limites de la API, se recomienda configurar la variable `SOCRATA_APP_TOKEN`.

## Procesamiento de datos realizado

Durante la preparacion de la informacion, el proyecto:

- normaliza nombres de columnas
- valida columnas obligatorias de la API
- convierte columnas numericas y fechas
- crea la columna `categoria_tarifa`
- calcula `ingreso_estimado`
- genera variables temporales como `periodo`, `anio` y `mes`
- calcula `tasa_evasion` y `porcentaje_exentos`

## Integrantes del grupo

- Diego Armando Romero Romero
- Keith Smith Balaguera Rodriguez
- Andres David Posada Patino

## Estado del archivo

Este `README.md` ya fue creado y guardado localmente en la ruta [README.md](c:/Users/posad/OneDrive/Escritorio/StreamLit/README.md).
