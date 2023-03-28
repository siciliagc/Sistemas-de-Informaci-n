import sqlite3
import numpy as np
import pandas as pd
from numpy import nan
import re
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
openPorts = pd.read_sql_query("SELECT analisisPuertosAbiertos as puertosAbiertos from devices", con)
openPorts.replace(to_replace=["NULL"], value=np.nan, inplace=True)
openPorts.dropna(inplace=True)
openPorts.reset_index(drop=True, inplace=True)
# Obtener el número de puertos de cada registro
openPorts['num_puertos'] = openPorts['puertosAbiertos'].apply(lambda x: len(re.findall(r'\d+', x)))
# Obtener el protocolo de cada puerto en cada registro
openPorts['TCP'] = openPorts['puertosAbiertos'].apply(lambda x: len([p for p in eval(x) if 'TCP' in p]))
openPorts['UDP'] = openPorts['puertosAbiertos'].apply(lambda x: len([p for p in eval(x) if 'UDP' in p]))
print(openPorts)

print(f"Media total de puertos abiertos: {openPorts['num_puertos'].mean():.2f}")
print(f"Desviación estándar total de puertos abiertos: {openPorts['num_puertos'].std():.2f}")
print(f"Media de puertos abiertos bajo TCP: {openPorts['TCP'].mean():.2f}")
print(f"Desviación estándar de puertos abiertos bajo TCP: {openPorts['TCP'].std():.2f}")
print(f"Media de puertos abiertos bajo TCP: {openPorts['UDP'].mean():.2f}")
print(f"Desviación estándar de puertos abiertos bajo TCP: {openPorts['UDP'].std():.2f}")

# Apartado d: Media y desviación estándar del número de servicios inseguros detectados
print(f"Media de servicios inseguros detectados: {df_devices['analisisServiviosInseguros'].mean():.2f}")
print(f"Desviación estándar de servicios inseguros detectados: {df_devices['analisisServiviosInseguros'].std():.2f}")

# Apartado e: Media y desviación estándar del número de vulnerabilidades detectadas
print(f"Media de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].mean():.2f}")
print(f"Desviación estándar de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].std():.2f}")

# Apartado f: Valor mínimo y valor máximo del total de puertos abiertos
print(f"Valor mínimo total de la cantidad de puertos: {openPorts['num_puertos'].min()}")
print(f"Valor máximo total de la cantidad de puertos: {openPorts['num_puertos'].max()}")
print(f"Valor mínimo de la cantidad de puertos bajo TCP: {openPorts['TCP'].min()}")
print(f"Valor máximo de la cantidad de puertos bajo TCP: {openPorts['TCP'].max()}")
print(f"Valor mínimo de la cantidad de puertos bajo UDP: {openPorts['UDP'].min()}")
print(f"Valor máximo de la cantidad de puertos bajo UDP: {openPorts['UDP'].max()}")


# Apartado g: Valor mínimo y valor máximo del número de vulnerabilidades detectadas
print(f"Valor mínimo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].min()}")
print(f"Valor máximo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].max()}")
