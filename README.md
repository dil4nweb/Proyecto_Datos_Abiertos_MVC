# Sistema Web de Consulta de Datos Abiertos de Colombia

**Asignatura:** Desarrollo de Aplicaciones con Acceso a Datos

**Integrantes:**
- Dilan Tapia Mercado
- Johan Duran Suarez
- Kevin Sanmiguel Ortiz

## Objetivo

Desarrollar una aplicación web utilizando Python y Flask que permita consultar información de una API pública del portal Datos Abiertos Colombia, almacenar los registros obtenidos en SQL Server y mostrarlos mediante una página web sencilla, aplicando la arquitectura Modelo-Vista-Controlador (MVC).

La aplicación permite consultar la API, guardar registros, evitar duplicados, realizar búsquedas y visualizar un resumen numérico de la información almacenada.

## Dataset seleccionado

- **Nombre:** Registro de Activos de Información.
- **Fuente:** Datos Abiertos Colombia (datos.gov.co).
- **Propósito:** consultar información sobre categorías de información pública, su descripción, disponibilidad, formato y medio de conservación.
- **Enlace del conjunto de datos:** https://www.datos.gov.co/d/sxi5-ie6w
- **Endpoint de la API:** https://www.datos.gov.co/resource/sxi5-ie6w.json?$limit=100

### Campos utilizados

- `nombre_o_t_tulo_de_la_categor`: nombre o título de la categoría.
- `descripci_n_del_contenido`: descripción del contenido.
- `idioma`: idioma de la información.
- `medio_de_conservaci_n_y_o`: medio de conservación o soporte.
- `formato`: formato de la información.
- `informaci_n_disponible`: indica si la información está disponible.
- `informaci_n_publicada`: indica si la información está publicada.

Para identificar los registros se utiliza una clave SHA-256 generada a partir del contenido JSON, evitando almacenar registros idénticos más de una vez.

## Requisitos

Para ejecutar el proyecto se necesitan las siguientes herramientas:

- Python 3.10 o superior.
- Visual Studio Code.
- SQL Server.
- SQL Server Management Studio (SSMS).
- Microsoft ODBC Driver 18 for SQL Server.
- Conexión a Internet.

## Instalación y ejecución

**1. Abrir el proyecto**

Abrir la carpeta `Proyecto_Datos_Abiertos_MVC` en Visual Studio Code.

**2. Crear el entorno virtual**

Abrir una terminal CMD y ejecutar:

```cmd
python -m venv venv
```

**3. Activar el entorno virtual**

```cmd
venv\Scripts\activate
```

**4. Instalar las dependencias**

```cmd
pip install -r requirements.txt
```

**5. Configurar SQL Server**

Abrir SQL Server Management Studio, conectarse al servidor y ejecutar el archivo `sql/crear_bd.sql`.

Este script crea la base de datos `DatosAbiertosDB` y la tabla `RegistrosAPI`.

**6. Configurar la conexión**

Crear el archivo `.env` a partir de `.env.example` y configurar los datos de conexión:

```env
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=DatosAbiertosDB
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUSTED=yes
DB_USER=
DB_PASSWORD=
API_RESOURCE_ID=sxi5-ie6w
SECRET_KEY=clave-local-para-el-proyecto
```

El nombre del servidor debe ajustarse según la configuración de SQL Server del equipo.

**7. Probar la API**

```cmd
python probar_api.py
```

Este comando permite comprobar que la API devuelve registros en formato JSON.

**8. Ejecutar la aplicación web**

```cmd
python app.py
```

**9. Abrir la aplicación**

Ingresar desde el navegador a:

http://127.0.0.1:5000

Desde la página principal se pueden realizar las siguientes operaciones:

- Consultar la API y guardar los registros en SQL Server.
- Visualizar los registros almacenados.
- Buscar información mediante filtros.
- Consultar un resumen numérico de los datos.

## Arquitectura MVC

El proyecto utiliza el patrón Modelo-Vista-Controlador (MVC), separando las responsabilidades de cada componente.

**Modelo (Model)**

Archivo: `models/datos_model.py`

Se encarga de establecer la conexión con SQL Server, almacenar los registros recibidos, evitar duplicados y realizar consultas a la base de datos.

**Vista (View)**

Archivos:
- `templates/index.html`
- `static/estilos.css`

Contiene la interfaz web que permite visualizar los registros, realizar búsquedas y ejecutar la sincronización de datos.

**Controlador (Controller)**

Archivo: `app.py`

Se encarga de recibir las solicitudes del navegador, coordinar las operaciones de la aplicación y enviar los resultados a la vista.

**Cliente API**

Archivo: `api/api_client.py`

Realiza las peticiones HTTP al portal Datos Abiertos Colombia y obtiene la información en formato JSON.

### Flujo de funcionamiento

1. El usuario ingresa a la aplicación desde el navegador.
2. El controlador Flask recibe la solicitud.
3. El cliente API consulta los datos del portal datos.gov.co.
4. El modelo almacena los registros recibidos en SQL Server.
5. El controlador consulta la información almacenada.
6. La vista HTML muestra los resultados al usuario.

## Evidencias del funcionamiento

Las capturas que demuestran el funcionamiento del proyecto se encuentran en la carpeta `evidencias`.

Estas incluyen:

- Respuesta JSON obtenida desde la API.
- Registros almacenados en SQL Server.
- Página principal de la aplicación web.
- Sincronización de registros.
- Consulta de información mediante filtros.
- Comprobación de que no se insertan registros duplicados.
