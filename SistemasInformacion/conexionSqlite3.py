import sqlite3


try:

    mi_conexion = sqlite3.connect("ETL_system.db")
    cursor = mi_conexion.cursor()
    cursor.execute("CREATE TABLE alerts (timestamp date, sid real, msg text, clasificacion text, prioridad real, protocolo text, origen text, destino text, puerto real) ")
    cursor.execute("CREATE TABLE devices (id text, ip real, localizacion text, responsable nombre, analisis puertos)")

except Exception as ex:
    print(ex)

