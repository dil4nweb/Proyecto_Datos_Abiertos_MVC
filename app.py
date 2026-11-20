import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from api.api_client import APIClient
from models.datos_model import guardar_registros, consultar_registros, resumen

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'solo-desarrollo-local-cambiar')

@app.get('/')
def inicio():
    filtro = request.args.get('q', '').strip()[:100]
    try:
        registros = consultar_registros(filtro)
        estadisticas = resumen()
        error = None
    except Exception as exc:
        registros = []
        estadisticas = {'total': 0, 'formatos': 0}
        error = f'No se pudo conectar a SQL Server: {exc}. Revisa .env y ejecuta sql/crear_bd.sql.'
    return render_template('index.html', registros=registros, filtro=filtro, estadisticas=estadisticas, error=error)

@app.post('/sincronizar')
def sincronizar():
    try:
        limite = int(request.form.get('limite', '100'))
        datos = APIClient().obtener_registros(limite)
        nuevos = guardar_registros(datos)
        flash(f'API consultada: {len(datos)} registros recibidos, {nuevos} nuevos guardados.', 'ok')
    except (ValueError, Exception) as exc:
        flash(f'Error al sincronizar: {exc}', 'error')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
