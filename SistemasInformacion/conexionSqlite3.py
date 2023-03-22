import sqlite3
import json
def createdb():
    try:
        mi_conexion = sqlite3.connect("ETL_system.db")
        cursor = mi_conexion.cursor()
        #cursor.execute("CREATE TABLE alerts (timestamp date, sid real, msg text, clasificacion text, prioridad real, protocolo text, origen text, destino text, puerto real) ")
        cursor.execute("CREATE TABLE devices (id text, ip text, localizacion text, responsableNombre text,responsableTlfn integer, responsableRol text, analisisPuertosAbiertos text, analisisServicios integer, analisisServiviosInseguros integer, analisisVulnerabilidades integer )")
        mi_conexion.close()
    except Exception as ex:
        print(ex)
def insertDevices(variables):
    print(variables)
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute('INSERT INTO devices(id,ip,localizacion,responsableNombre,responsableTlfn,responsableRol,analisisPuertosAbiertos,analisisServicios,analisisServiviosInseguros,analisisVulnerabilidades) VALUES (?,?,?,?,?,?,?,?,?,?)',variables)
    con.commit()
    con.close()


def insertAlerts():
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute("INSERT INTO alerts ")
    con.close()

#createdb()
#insertAlerts()
file = open("devices.json")
dictDevices = json.load(file)
file.close()

leerPuertos = eval("['8080/TCP', '3306/TCP', '3306/UDP']")
print(leerPuertos)
#for i in dictDevices:
    #print(i['responsable'])
    #insertDevices((i['id'],i['ip'],i['localizacion'],i['responsable']['nombre'],i['responsable']['telefono'],i['responsable']['rol'],str(i['analisis']['puertos_abiertos']),i['analisis']['servicios'],i['analisis']['servicios_inseguros'],i['analisis']['vulnerabilidades_detectadas']))