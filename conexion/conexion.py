"""Conexion PostgreSQL configurada mediante variables de entorno."""
import os
import psycopg2


def get_db():
    database_url = os.environ.get('DATABASE_URL', '').strip()
    if not database_url:
        raise RuntimeError('Configura DATABASE_URL antes de iniciar la aplicacion.')
    return psycopg2.connect(database_url, sslmode='require', connect_timeout=15)
