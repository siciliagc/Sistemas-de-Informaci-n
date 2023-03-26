import sqlite3
import json
import csv
def createdb():
    try:
        mi_conexion = sqlite3.connect("ETL_system.db")
        cursor = mi_conexion.cursor()
        cursor.execute('CREATE TABLE alerts (timestamp date, sid real, msg text, clasificacion text, prioridad real, protocolo text, origen text, destino text, puerto real) ')
        cursor.execute('CREATE TABLE devices (id text, ip text, localizacion text, responsableNombre text,responsableTlfn integer, responsableRol text, analisisPuertosAbiertos text, analisisServicios integer, analisisServiviosInseguros integer, analisisVulnerabilidades integer )')
        mi_conexion.close()
    except Exception as ex:
        print(ex)

def missingToCero(originalValue):
    newValue = 'NULL'
    if originalValue != "None":
        newValue = originalValue
    return newValue

def insertDevices(variables):
    #print(variables)
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute('INSERT INTO devices(id,ip,localizacion,responsableNombre,responsableTlfn,responsableRol,analisisPuertosAbiertos,analisisServicios,analisisServiviosInseguros,analisisVulnerabilidades) VALUES (?,?,?,?,?,?,?,?,?,?)',variables)
    con.commit()
    con.close()

def insertAlerts(variables):
    con = sqlite3.connect("ETL_system.db")
    cur = con.cursor()
    cur.execute('INSERT INTO alerts(timestamp,sid,msg,clasificacion,prioridad,protocolo,origen,destino,puerto)VALUES (?,?,?,?,?,?,?,?,?)', variables)
    con.commit()
    con.close()

def loadCsv():
    with open('alerts.csv', newline='') as csvfile:
        datos = csv.DictReader(csvfile)
        for fila in datos:
            insertAlerts((fila['timestamp'], fila['sid'], fila['msg'], fila['clasificacion'], fila['prioridad'], fila['protocolo'], fila['origen'], fila['destino'], fila['puerto']))

def loadJson():
    file = open("devices.json")
    dictDevices = json.load(file)
    file.close()
    for i in dictDevices:
        #print(i['responsable'])
        insertDevices((missingToCero(i['id']), missingToCero(i['ip']), missingToCero(i['localizacion']), missingToCero(i['responsable']['nombre']), missingToCero(i['responsable']['telefono']), missingToCero(i['responsable']['rol']), missingToCero(str(i['analisis']['puertos_abiertos'])), missingToCero(i['analisis']['servicios']), missingToCero(i['analisis']['servicios_inseguros']), missingToCero(i['analisis']['vulnerabilidades_detectadas'])))

#createdb()
#loadJson()
#loadCsv()

