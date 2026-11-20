import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    def __init__(self):
        recurso = os.getenv("API_RESOURCE_ID", "sxi5-ie6w")
        self.url = f"https://www.datos.gov.co/resource/{recurso}.json"

    def obtener_registros(self, limite=100):
        limite = max(1, min(int(limite), 500))
        respuesta = requests.get(self.url, params={"$limit": limite}, timeout=25)
        respuesta.raise_for_status()
        datos = respuesta.json()
        if not isinstance(datos, list):
            raise ValueError("La API no devolvio una lista JSON")
        return datos
