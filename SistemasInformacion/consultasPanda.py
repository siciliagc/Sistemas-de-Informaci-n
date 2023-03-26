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
"""""
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
# Debemos hallar la manera de crear el siguiente dataframe:
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

# Función para obtener los puertos únicamente:
def obtenerPuertos(tupla):
    for puerto in tupla:
        puerto = puerto.split("/")
        print(puerto[0])  # Esto nos imprime por pantalla el puerto, pero creo que nos puede servir para este apartado :)


# Apartado g: Valor mínimo y valor máximo del número de vulnerabilidades detectadas
print(f"Valor mínimo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].min()}")
print(f"Valor máximo de vulnerabilidades detectadas: {df_devices['analisisVulnerabilidades'].max()}")

##############
# Ejercicio 3#
##############
# Agrupación por permisos:

alertas_permisos = df_alerts.groupby('permisos')['clasificacion']

# Agrupación por fecha:

df_alerts['timestamp'] = pd.to_datetime(df_alerts['timestamp'], format='%Y-%m-%d %H:%M:%S')

alertas_julio = df_alerts.loc[(df_alerts['timestamp'].dt.month == 7)]
alertas_agosto = df_alerts.loc[(df_alerts['timestamp'].dt.month == 8)]

#############
# APARTADO A#
#############

# Número de observaciones por permiso:
print("Número de observaciones para alertas del tipo 1: ", alertas_permisos.sum()[1.0])

print("Número de observaciones para alertas del tipo 2: ", alertas_permisos.sum()[2.0])

print("Número de observaciones para alertas del tipo 3: ", alertas_permisos.sum()[3.0])

# Número de observaciones por fecha:
# Julio:
num_obervaciones_julio = alertas_julio.groupby('timestamp')['clasificacion'].count()
print("Numero observaciones julio: ", num_obervaciones_julio)
num_obervaciones_agosto = alertas_agosto.groupby('timestamp')['clasificacion'].count()

# Agosto:
print("Número observaciones agosto: ", num_obervaciones_agosto)

#############
# APARTADO B#
#############


#############
# APARTADO C#
#############

# Por tipo de alerta:
print("Mediana con alertas del tipo 1: ", alertas_permisos.median()[1.0])
print("Mediana con alertas del tipo 2: ", alertas_permisos.median()[2.0])
print("Mediana con alertas del tipo 3: ", alertas_permisos.median()[3.0])

# Por mes:
print("Mediana con alertas en julio ", alertas_julio.groupby('timestamp')['clasificacion'].median())
print("Mediana con alertas en agosto: ", alertas_agosto.groupby('timestamp')['clasificacion'].median())


#############
# APARTADO D#
#############
# Por tipo de alerta:
print("Media con alertas del tipo 1: ", alertas_permisos.mean()[1.0])
print("Media con alertas del tipo 2: ", alertas_permisos.mean()[2.0])
print("Media con alertas del tipo 3: ", alertas_permisos.mean()[3.0])

# Por mes:
print("Media con alertas en julio ", alertas_julio.groupby('timestamp')['clasificacion'].mean())
print("Media con alertas en agosto: ", alertas_agosto.groupby('timestamp')['clasificacion'].mean())


#############
# APARTADO E#
#############
# Por tipo de alerta:
print("Varianza con alertas del tipo 1: ", alertas_permisos.var(ddof=0)[1.0])
print("Varianza con alertas del tipo 2: ", alertas_permisos.var(ddof=0)[2.0])
print("Varianza con alertas del tipo 3: ", alertas_permisos.var(ddof=0)[3.0])

# Por mes:
print("Varianza con alertas en julio ", alertas_julio.groupby('timestamp')['clasificacion'].var(ddof=0))
print("Varianza con alertas en agosto: ", alertas_agosto.groupby('timestamp')['clasificacion'].var(ddof=0))


#############
# APARTADO F#
#############
# Máximos:
# Por tipo de alerta:
print("Máximo con alertas del tipo 1: ", alertas_permisos.max()[1.0])
print("Máximo con alertas del tipo 2: ", alertas_permisos.max()[2.0])
print("Máximo con alertas del tipo 3: ", alertas_permisos.max()[3.0])

# Por mes:
print("Máximo con alertas en julio ", alertas_julio.groupby('timestamp')['clasificacion'].max())
print("Máximo con alertas en agosto: ", alertas_agosto.groupby('timestamp')['clasificacion'].max())

# Mínimos:

print("Mínimo con alertas del tipo 1: ", alertas_permisos.min()[1.0])
print("Mínimo con alertas del tipo 2: ", alertas_permisos.min()[2.0])
print("Mínimo con alertas del tipo 3: ", alertas_permisos.min()[3.0])

# Por mes:
print("Mínimo con alertas en julio ", alertas_julio.groupby('timestamp')['clasificacion'].min())
print("Mínimo con alertas en agosto: ", alertas_agosto.groupby('timestamp')['clasificacion'].min())

"""

##############
# Ejercicio 4#
##############

#############
# APARTADO A#
#############

ip_mas_problematicas_df = df_alerts[df_alerts['prioridad']==1]
ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(name='numero_alertas')
ip_mas_problematicas_df.sort_values(by=['numero_alertas'],ascending=False, inplace=True)
ip_mas_problematicas_df.head(10).plot(title='Top 10 direcciones IPs más problemáticas', x="origen", y="numero_alertas", kind="bar")
plt.show()

#############
# APARTADO C#
#############

alertas_por_categoria = df_alerts.groupby('clasificacion')['clasificacion'].count().reset_index(name='numero_alertas')
alertas_por_categoria.plot(title='Alertas por Categoría', x='clasificacion', y='numero_alertas', kind='bar')
plt.xticks(fontsize=8)
plt.show()

#############
# APARTADO D#
#############