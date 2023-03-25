import hashlib
import sqlite3
from typing import List
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import nan
con = sqlite3.connect('ETL_system.db')
cur = con.cursor()


##############
# Ejercicio 2#
##############
def convertArray(columns: List[str]) -> str:
    string_result: str = columns[0]
    for c in range(1, len(columns)):
        string_result = string_result + ", " + columns[c]
    return string_result

def fetch_tables(table: str, columns: str):
    cur.execute("SELECT "+ columns+ "FROM "+ table)
    return cur.fetchall()


def createDataframe(table: str, columns: list[str]):
    return pd.DataFrame(fetch_tables(table, convertArray(columns)), columns=columns)


# Dataframe para devices:
#devices_and_none = createDataframe("devices", ["id", "ip", "localizacion", "responsableNombre", "responsableTlfn", "responsableRol", "analisisPuertosAbiertos", "analisisServicios", "analisisServiviosInseguros", "analisisVulnerabilidades"])

# Apartado a: Número de dispositivos (y campos missing o None).

df_devices = pd.read_sql_query("SELECT * from devices", con)
print(f"Número de dispositivos: {df_devices['id'].unique().size}")
print(f"Número total de campos incluyendo los missing: {df_devices.count().sum()}")
df_devices.replace(to_replace=["None"], value=nan, inplace=True)
print(f"Número total de campos excluyendo los missing: {df_devices.count().sum()}")
# Apartado b: Número de alertas
df_alerts = pd.read_sql_query("SELECT * from alerts", con)
print(f"Número de alertas: {df_alerts['timestamp'].size}")
#Apartado c: Media
openPorts = pd.Series(df_devices['analisisPuertosAbiertos'][0])
print(openPorts)
size = 14
for i in range(size):
    if df_devices['analisisPuertosAbiertos'][i] != nan:
        new = openPorts.append(pd.Series(df_devices['analisisPuertosAbiertos'][i]))

print(new)


#print("Dispositivos missing: ", devices_and_none.count().sum())
#devices_and_none[devices_and_none['id']==0].count().sum()
#+ devices_and_none[devices_and_none['ip']==0].count().sum()
#+ devices_and_none[devices_and_none['localizacion']==0].count().sum()
#+ devices_and_none[devices_and_none['responsableNombre']==0].count().sum()
#+ devices_and_none[devices_and_none['responsableTlfn']==0].count().sum()
#+ devices_and_none[devices_and_none['responsableRol']==0].count().sum()
#+ devices_and_none[devices_and_none['analisisPuertosAbiertos']==0].count().sum()
#+ devices_and_none[devices_and_none['analisisServicios']==0].count().sum()
#+ devices_and_none[devices_and_none['analisisServiviosInseguros']==0].count().sum()
#+ devices_and_none[devices_and_none['analisisVulnerabilidades']==0].count().sum())



