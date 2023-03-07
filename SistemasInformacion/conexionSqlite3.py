import sqlite3

try:
    mi_conexion = sqlite3.connect("devices.db")
    cursor = mi_conexion.cursor()
    cursor.execute("CREATE TABLE ")