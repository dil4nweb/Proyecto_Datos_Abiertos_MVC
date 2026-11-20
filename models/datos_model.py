import os
import json
import hashlib
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# Campos reales documentados en el dataset sxi5-ie6w.
CAMPOS = {
    "titulo": "nombre_o_t_tulo_de_la_categor",
    "descripcion": "descripci_n_del_contenido",
    "idioma": "idioma",
    "medio": "medio_de_conservaci_n_y_o",
    "formato": "formato",
    "disponible": "informaci_n_disponible",
    "publicada": "informaci_n_publicada",
}

def obtener_conexion():
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    servidor = os.getenv("DB_SERVER", "localhost")
    base = os.getenv("DB_NAME", "DatosAbiertosDB")
    partes = [f"DRIVER={{{driver}}}", f"SERVER={servidor}", f"DATABASE={base}", "Encrypt=yes", "TrustServerCertificate=yes", "Connection Timeout=8"]
    if os.getenv("DB_TRUSTED", "yes").lower() in ("yes", "true", "1"):
        partes.append("Trusted_Connection=yes")
    else:
        usuario = os.getenv("DB_USER", "")
        clave = os.getenv("DB_PASSWORD", "")
        if not usuario or not clave:
            raise ValueError("Configura DB_USER y DB_PASSWORD en .env")
        partes.extend([f"UID={usuario}", f"PWD={clave}"])
    return pyodbc.connect(';'.join(partes) + ';')

def normalizar(registro):
    if not isinstance(registro, dict):
        raise ValueError("Registro JSON invalido")
    # No hay ID de fila garantizado en este dataset: clave SHA256 del contenido canonico.
    original = json.dumps(registro, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    identificador = hashlib.sha256(original.encode('utf-8')).hexdigest()
    valores = [str(registro.get(campo) or '')[:500] for campo in CAMPOS.values()]
    return (identificador, *valores, original)

def guardar_registros(registros):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0
    try:
        for registro in registros:
            datos = normalizar(registro)
            cursor.execute("""
                INSERT INTO dbo.RegistrosAPI
                (id_api, titulo, descripcion, idioma, medio, formato, disponible, publicada, json_original)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM dbo.RegistrosAPI WITH (UPDLOCK, HOLDLOCK) WHERE id_api = ?)
            """, *datos, datos[0])
            if cursor.rowcount > 0:
                insertados += 1
        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()

def consultar_registros(filtro=''):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        patron = '%' + filtro[:100] + '%'
        cursor.execute("""
            SELECT TOP (100) id_api, titulo, descripcion, idioma, medio, formato, disponible, publicada
            FROM dbo.RegistrosAPI
            WHERE titulo LIKE ? OR descripcion LIKE ? OR formato LIKE ? OR idioma LIKE ?
            ORDER BY id DESC
        """, patron, patron, patron, patron)
        columnas = [c[0] for c in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()

def resumen():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM dbo.RegistrosAPI")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT NULLIF(formato, '')) FROM dbo.RegistrosAPI")
        formatos = cursor.fetchone()[0]
        return {"total": total, "formatos": formatos}
    finally:
        cursor.close()
        conexion.close()
