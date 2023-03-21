import sqlite3
def createdb():
    try:
        mi_conexion = sqlite3.connect("ETL_system.db")
        cursor = mi_conexion.cursor()
        #cursor.execute("CREATE TABLE alerts (timestamp date, sid real, msg text, clasificacion text, prioridad real, protocolo text, origen text, destino text, puerto real) ")
        cursor.execute("CREATE TABLE devices (id text, ip text, localizacion text, responsableNombre text,responsableTlfn text, responsableRol text, analisisPuertosAbiertos text, analisisServicios real, analisisServiviosInseguros real, analisisVulnerabilidades real )")
        mi_conexion.close()
    except Exception as ex:
        print(ex)
def inserdb():
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute("INSERT INTO devices ")
    con.close()

createdb()