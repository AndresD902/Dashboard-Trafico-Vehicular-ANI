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
Dashboard-Trafico-Vehicular-ANI/
|-- .dockerignore
|-- .streamlit/
|   |-- config.toml
|-- app.py
|-- Dockerfile
|-- README.md
|-- render.yaml
|-- requirements.txt
|-- datos/
|   |-- __init__.py
|   |-- cliente_api.py
|   |-- cargador.py
|-- paginas/
|   |-- 1_resumen.py
|   |-- 2_analisis.py
|   |-- 3_datos.py
|-- procesamiento/
|   |-- __init__.py
|   |-- limpieza.py
|   |-- metricas.py
|   |-- transformaciones.py
|-- utilidades/
|   |-- __init__.py
|   |-- configuracion.py
|-- visualizaciones/
|   |-- __init__.py
|   |-- graficos.py
|   |-- panel.py
```

## Arquitectura del proyecto

El proyecto sigue una arquitectura modular por capas, donde cada carpeta tiene una responsabilidad concreta dentro del flujo de datos del dashboard.

### Capas principales

- `app.py`: punto de entrada de la aplicacion. Configura Streamlit, aplica estilos globales y registra la navegacion entre paginas.
- `datos/`: capa de acceso a datos. Se encarga de conectarse a la API publica de `datos.gov.co`, realizar las peticiones HTTP y centralizar la carga inicial.
- `procesamiento/`: capa de negocio y transformacion. Limpia los registros, valida columnas, convierte tipos de datos, calcula variables derivadas y aplica filtros.
- `visualizaciones/`: capa de presentacion analitica. Construye componentes visuales, metricas, paneles e indicadores con Streamlit y Plotly.
- `paginas/`: capa de vistas. Organiza el dashboard en secciones funcionales como `Resumen`, `Analisis` y `Datos`.
- `utilidades/`: capa de soporte. Centraliza configuraciones globales, variables de entorno, estilos y constantes reutilizables.

### Flujo general de la aplicacion

```text
API publica datos.gov.co
        |
        v
datos/cliente_api.py
        |
        v
datos/cargador.py
        |
        v
procesamiento/limpieza.py
        |
        v
procesamiento/transformaciones.py + procesamiento/metricas.py
        |
        v
visualizaciones/panel.py + visualizaciones/graficos.py
        |
        v
paginas/*.py
        |
        v
app.py
```

### Patron aplicado

La solucion se apoya en una separacion por responsabilidades similar a una arquitectura en capas:

- adquisicion de datos
- preparacion y transformacion
- calculo de indicadores
- presentacion visual
- navegacion de la aplicacion

Este enfoque facilita el mantenimiento, porque permite modificar la fuente de datos, las reglas de procesamiento o las visualizaciones sin reescribir toda la aplicacion.

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

## Docker

1. Construir la imagen:

```bash
docker build -t dashboard-peajes-colombia .
```

2. Ejecutar el contenedor localmente:

```bash
docker run --rm -p 10000:10000 ^
  -e API_PEAJES_URL=https://www.datos.gov.co/resource/8yi9-t44c.json ^
  -e LIMITE_API=50000 ^
  -e SOCRATA_APP_TOKEN= ^
  dashboard-peajes-colombia
```

3. Abrir la aplicacion en `http://localhost:10000`

Tambien puedes cargar tu archivo `.env` al contenedor:

```bash
docker run --rm -p 10000:10000 --env-file .env dashboard-peajes-colombia
```

## Despliegue en Render

El proyecto incluye `Dockerfile` y `render.yaml`, por lo que puede desplegarse en Render usando una imagen Docker. Si se desea mayor estabilidad frente a limites de la API, se recomienda configurar la variable `SOCRATA_APP_TOKEN`.

### Opcion 1. Usando Blueprint con `render.yaml`

1. Subir este repositorio a GitHub.
2. Entrar a Render y elegir `New` > `Blueprint`.
3. Conectar el repositorio.
4. Confirmar la creacion del servicio `dashboard-peajes-colombia`.
5. En Render, agregar el valor real de `SOCRATA_APP_TOKEN` en las variables de entorno.
6. Ejecutar el despliegue.

### Opcion 2. Creando el servicio manualmente

1. Entrar a Render y elegir `New` > `Web Service`.
2. Conectar el repositorio de GitHub.
3. En `Environment`, seleccionar `Docker`.
4. Verificar que Render detecte el `Dockerfile`.
5. Configurar estas variables de entorno:

```env
API_PEAJES_URL=https://www.datos.gov.co/resource/8yi9-t44c.json
LIMITE_API=50000
SOCRATA_APP_TOKEN=
```

6. Crear el servicio y esperar a que termine el build.

### Verificacion posterior al despliegue

- Abrir la URL publica generada por Render.
- Confirmar que carguen las paginas `Resumen`, `Analisis` y `Datos`.
- Si la API responde con restricciones o errores de acceso, configurar `SOCRATA_APP_TOKEN` y redeployar.

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
