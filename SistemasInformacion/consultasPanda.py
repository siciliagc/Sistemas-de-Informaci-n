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

# Apartado a: Número de dispositivos (y campos missing o None).
df_devices = pd.read_sql_query("SELECT * from devices", con)
print(f"Número de dispositivos: {df_devices.__len__()}")
df_devices.replace(to_replace=["NULL"], value=nan, inplace=True)
print(f"Número total de campos missing: {df_devices.isna().sum().sum()}")
print(f"Número total de campos excluyendo los missing: {df_devices.count().sum()}")
print(f"Número total de campos, incluyendo missing: {df_devices.isna().count().sum()}")

# Apartado b: Número de alertas
df_alerts = pd.read_sql_query("SELECT * from alerts", con)
print(f"Número de alertas: {df_alerts['timestamp'].size}")

# Apartado c: Media y desviación estándar del total de puertos abiertos
print(df_devices['analisisPuertosAbiertos'])
print(df_devices.shape)
openPorts = df_devices.dropna(subset=['analisisPuertosAbiertos'])
print(openPorts.shape)
openPorts = openPorts.explode('analisisPuertosAbiertos')
print(openPorts.shape)
openPorts = openPorts.reset_index(drop=True)
openPorts[['puerto', 'protocolo']] = openPorts['analisisPuertosAbiertos'].str.split('/', expand=True)
openPorts['puerto'] = pd.to_numeric(openPorts['puerto'])
openPorts.drop('analisisPuertosAbiertos', axis=1, inplace=True)

print(f"Media de puertos abiertos: {openPorts['puerto'].mean()}")
print(f"Desviación estandar de puertos abiertos: {openPorts['puerto'].std()}")

# Apartado d: Media y desviación estándar del número de servicios inseguros detectados
print(f"Media de servicios inseguros detectados: {df_devices['analisisServiciosInseguros'].mean()}")
print(f"Desviación estandar de servicios inseguros detectados: {df_devices['analisisServiciosInseguros'].std()}")

# Apartado e: Media y desviación estándar del número de vulnerabilidades detectadas
print(f"Media de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].mean()}")
print(f"Desviación estandar de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].std()}")

# Apartado f: Valor mínimo y valor máximo del total de puertos abiertos

# Tenemos 7 dispositivos, y cada uno tiene un número de puertos abiertos diferentes, almacenados en un array
# Debemos allar la manera de crear el siguiente dataframe:
# | dispositivo | puerto |
# | ELK         | 9200   |
# | ELK         | 80     |
# | ELK         | 443    |
# | web         | 80     |
# | web         | 443    |
# | paco_pc     | NaN    |
# o quizás así es más correcto:
# | ELK         | web    | paco_pc |
# | 9200        | 80     | NaN     |
# | 80          | 443    | NaN     |
# | 443         | NaN    | NaN     |

# Apartado g: Valor mínimo y valor máximo del número de vulnerabilidades detectadas
print(f"Valor mínimo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].min()}")
print(f"Valor máximo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].max()}")





