# Sistema web de consulta de datos abiertos de Colombia

**Asignatura:** Desarrollo de Aplicaciones con Acceso a Datos  
**Integrantes:** Dilan Tapia Mercado, Johan Duran Suarez y Kevin Sanmiguel Ortiz.

## Objetivo
Consumir una API pública JSON de datos.gov.co con Python, guardar registros en SQL Server mediante pyodbc y consultar desde una web Flask con patrón MVC, filtro y resumen numérico.

## Dataset seleccionado
- **Nombre:** Registro de Activos de Información.
- **Propósito:** describir las categorías de información pública y su disponibilidad, formato y soporte.
- **Ficha:** https://www.datos.gov.co/Funci-n-P-blica/Registro-de-Activos-de-Informaci-n/sxi5-ie6w
- **Endpoint:** https://www.datos.gov.co/resource/sxi5-ie6w.json?$limit=100
- **Campos del JSON:** `nombre_o_t_tulo_de_la_categor` (título), `descripci_n_del_contenido` (descripción), `idioma`, `medio_de_conservaci_n_y_o` (soporte), `formato`, `informaci_n_disponible` (disponibilidad), `informaci_n_publicada` (publicación).
- **Clave única:** SHA-256 del JSON completo ordenado por claves; el dataset no garantiza un ID de fila en la respuesta. Esto impide insertar dos veces un registro idéntico, pero si el contenido cambia se registra como una nueva versión.

## Requisitos Windows
Python 3.10 o superior, VS Code, SQL Server (Express/Developer) con servicio activo, SQL Server Management Studio (SSMS), Microsoft ODBC Driver 18 for SQL Server, conexión a Internet.

## Instalación en VS Code
1. Descomprimir ZIP y abrir la carpeta `Proyecto_Datos_Abiertos_MVC` con **Archivo > Abrir carpeta**.
2. Abrir Terminal > Nueva terminal (PowerShell).
3. Ejecutar `py -m venv venv`.
4. Ejecutar `./venv/Scripts/python.exe -m pip install -r requirements.txt` (en PowerShell también funciona `.\venv\Scripts\python.exe -m pip install -r requirements.txt`).
5. Copiar `.env.example` como `.env` y ajustar `DB_SERVER` al nombre que muestra SSMS, por ejemplo `localhost\SQLEXPRESS` para una instancia Express, o `localhost` para la instancia predeterminada. `DB_TRUSTED=yes` usa autenticación de Windows. Para autenticación SQL usa `DB_TRUSTED=no`, `DB_USER` y `DB_PASSWORD`.
6. En SSMS, conectar al servidor, abrir `sql/crear_bd.sql` y ejecutar todo el script (F5). Confirmar que exista `DatosAbiertosDB`.
7. Probar API: `.\venv\Scripts\python.exe probar_api.py`.
8. Iniciar web: `.\venv\Scripts\python.exe app.py`.
9. Abrir http://127.0.0.1:5000, pulsar **Consultar API y guardar en SQL Server**, luego buscar una palabra visible en la tabla.
10. Para detener, presionar Ctrl+C en la terminal.

Si PowerShell impide activar scripts, **no necesitas activar el entorno**: ejecuta directamente `venv\Scripts\python.exe` como se indica arriba.

## Estructura MVC
- **Controlador:** `app.py`, rutas GET `/` y POST `/sincronizar`.
- **Modelo:** `models/datos_model.py`, conexión, inserciones parametrizadas, SELECT y resumen.
- **Vista:** `templates/index.html` y `static/estilos.css`, sin SQL.
- **Servicio API:** `api/api_client.py`, petición HTTP con requests y validación JSON.
- **SQL:** `sql/crear_bd.sql`.

**Flujo:** navegador → controlador Flask → cliente API → JSON → modelo SQL Server → controlador → vista HTML.

## Pruebas
- `python -m unittest discover -s tests -v` prueba la clave determinista sin necesidad de SQL Server.
- Ejecutar sincronización y comprobar en SSMS: `SELECT COUNT(*) FROM dbo.RegistrosAPI;`.
- Sincronizar de nuevo los mismos registros: no deben insertarse duplicados idénticos.
- Buscar por título, descripción, idioma o formato.
- Evidencias: seguir `evidencias/INSTRUCCIONES.md` y agregar capturas reales.

## Problemas frecuentes
- `IM002` / driver no encontrado: instalar ODBC Driver 18 y verificar `DB_DRIVER`.
- `Login failed`: revisar usuario, permisos y tipo de autenticación.
- `08001`: comprobar nombre de instancia SQL Server y servicio activo.
- `Invalid object name`: ejecutar el script SQL en la base correcta.
- HTTP 404/429: revisar endpoint o esperar antes de reintentar.
- No subir `.env`, `venv/`, contraseñas ni archivos generados al repositorio.


