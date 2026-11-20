from api.api_client import APIClient
import json

datos = APIClient().obtener_registros(3)
print('Registros recibidos:', len(datos))
print(json.dumps(datos[:1], ensure_ascii=False, indent=2))
