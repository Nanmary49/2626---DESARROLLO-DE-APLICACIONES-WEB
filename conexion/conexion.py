# ================================================================
# conexion/conexion.py
# Conexión centralizada con MySQL
# Narvi Collector Scale Models — Semana 13
# ================================================================

import mysql.connector

def get_db():
    """
    Establece y retorna la conexión con la base de datos MySQL.
    Centralizar la conexión permite cambiarla fácilmente.
    """
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='narvi_db'
    )
    return conexion