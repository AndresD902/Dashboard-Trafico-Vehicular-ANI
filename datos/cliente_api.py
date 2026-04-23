from __future__ import annotations

from typing import Any

import pandas as pd
import requests

from utilidades.configuracion import obtener_configuracion


class ClienteAPI:
    def __init__(self) -> None:
        self.configuracion = obtener_configuracion()

    def _encabezados(self) -> dict[str, str]:
        encabezados = {"Accept": "application/json"}
        if self.configuracion.token_app:
            encabezados["X-App-Token"] = self.configuracion.token_app
        return encabezados

    def obtener_registros(self) -> pd.DataFrame:
        registros: list[dict[str, Any]] = []
        offset = 0
        limite = self.configuracion.limite_por_peticion

        while True:
            try:
                respuesta = requests.get(
                    self.configuracion.url_base,
                    params={
                        "$limit": limite,
                        "$offset": offset,
                        "$order": "hasta ASC",
                    },
                    headers=self._encabezados(),
                    timeout=self.configuracion.tiempo_espera,
                )
            except requests.RequestException as error:
                raise RuntimeError(
                    "No fue posible conectarse con la API publica de datos.gov.co."
                ) from error

            if respuesta.status_code in {401, 403}:
                raise RuntimeError(
                    "La API rechazo la solicitud. Verifica si el token configurado es valido."
                )

            try:
                respuesta.raise_for_status()
            except requests.HTTPError as error:
                raise RuntimeError(
                    f"La API devolvio un error HTTP {respuesta.status_code}."
                ) from error

            lote = respuesta.json()
            if not lote:
                break

            registros.extend(lote)

            if len(lote) < limite:
                break

            offset += limite

        return pd.DataFrame(registros)
