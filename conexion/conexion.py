# ================================================================
# conexion/conexion.py
# Conexión centralizada con PostgreSQL (Render)
# Narvi Collector Scale Models — Semana 15
# ================================================================

import psycopg2
import os

def get_db():
    """
    Establece y retorna la conexión con PostgreSQL en Render.
    Usa DATABASE_URL si está disponible (producción en Render),
    o los datos locales si no existe (desarrollo local).
    """
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Conexión en Render usando variable de entorno
        conn = psycopg2.connect(database_url, sslmode='require')
    else:
        # Conexión local para desarrollo
        conn = psycopg2.connect(
            host='dpg-daq4l9egekts73bij5e0-a.oregon-postgres.render.com',
            port=5432,
            database='narvi_db',
            user='narvi_db_user',
            password='zxoZ0NyCPiJmt7xmo9IKPhPgqF9YOhLD',
            sslmode='require'
        )
    return conn