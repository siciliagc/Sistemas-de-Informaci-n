import sqlite3
def createdb():
    try:
        mi_conexion = sqlite3.connect("ETL_system.db")
        cursor = mi_conexion.cursor()
        #cursor.execute("CREATE TABLE alerts (timestamp date, sid real, msg text, clasificacion text, prioridad real, protocolo text, origen text, destino text, puerto real) ")
        cursor.execute("CREATE TABLE devices (id text, ip text, localizacion text, responsableNombre text,responsableTlfn integer, responsableRol text, analisisPuertosAbiertos text, analisisServicios integer, analisisServiviosInseguros integer, analisisVulnerabilidades integer )")
        mi_conexion.close()
    except Exception as ex:
        print(ex)
def insertDevices():
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute("INSERT INTO devices VALUES ('')")
    con.close()


def insertAlerts():
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute("INSERT INTO alerts ")
    con.close()

createdb()
insertAlerts()
insertDevices()