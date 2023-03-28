import re
import sqlite3
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
##############
# Ejercicio 3#
##############

# Merge tables:
alerts_devices = pd.read_sql_query("SELECT * FROM alerts JOIN devices ON (alerts.origen = devices.ip OR alerts.destino = devices.ip)", con)
# Agrupación por permisos:
alertas_permisos_1 = alerts_devices[alerts_devices['prioridad'] == 1]
alertas_permisos_2 = alerts_devices.loc[alerts_devices['prioridad'] == 2]
alertas_permisos_3 = alerts_devices.loc[alerts_devices['prioridad'] == 3]

# Agrupación por fecha:
alerts_devices['timestamp'] = pd.to_datetime(alerts_devices['timestamp'], format='%Y-%m-%d %H:%M:%S')
alertas_julio = alerts_devices.loc[(alerts_devices['timestamp'].dt.month == 7)]
alertas_agosto = alerts_devices.loc[(alerts_devices['timestamp'].dt.month == 8)]


#############
# APARTADO A#
#############

# Número de observaciones por permiso:

print(f"Número de alertas con prioridad 1: {alertas_permisos_1.__len__()}")
print(f"Número de alertas con prioridad 2: {alertas_permisos_2.__len__()}")
print(f"Número de alertas con prioridad 3: {alertas_permisos_3.__len__()}")


# Número de observaciones por fecha:
# Julio:
print(f"Numero observaciones julio: {alertas_julio.__len__()}")
# Agosto:
print(f"Número observaciones agosto: {alertas_agosto.__len__()}")

#############
# APARTADO B#
#############
df_none_alertas_permisos_1 = alertas_permisos_1.loc[alertas_permisos_1['localizacion'] == 'NULL']
df_none_alertas_permisos_2 = alertas_permisos_2.loc[alertas_permisos_2['localizacion'] == 'NULL']
df_none_alertas_permisos_3 = alertas_permisos_3.loc[alertas_permisos_3['localizacion'] == 'NULL']
df_none_julio = alertas_julio.loc[alertas_julio['localizacion'] == 'NULL']
df_none_agosto = alertas_agosto.loc[alertas_agosto['localizacion'] == 'NULL']

# Número de observaciones none por permiso:
print("Número de observaciones 'None' para alertas del tipo 1: ", len(df_none_alertas_permisos_1))
print("Número de observaciones 'None' para alertas del tipo 2: ", len(df_none_alertas_permisos_2))
print("Número de observaciones 'None' para alertas del tipo 3: ", len(df_none_alertas_permisos_3))

# Julio:
num_none_julio = len(df_none_julio.groupby('timestamp')['clasificacion'])
print("Numero observaciones 'None' julio: ", num_none_julio)

# Agosto:
num_none_agosto = len(df_none_agosto.groupby('timestamp')['clasificacion'])
print("Número observaciones 'None' agosto: ", num_none_agosto)

#############
# APARTADO C#
#############
# Por prioridad:
mediana_por_prioridad = alerts_devices.groupby('prioridad')['analisisVulnerabilidades'].median()
print("Mediana por prioridad: ", mediana_por_prioridad)

# Por fecha:
mediana_por_fecha_julio = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([7]), 'analisisVulnerabilidades'].median()
print("Mediana por fecha (Julio): ", mediana_por_fecha_julio)
mediana_por_fecha_agosto = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([8]), 'analisisVulnerabilidades'].median()
print("Mediana por fecha (Agosto): ", mediana_por_fecha_agosto)


#############
# APARTADO D#
#############
# Por prioridad
media_por_prioridad = alerts_devices.groupby('prioridad')['analisisVulnerabilidades'].mean()
print("Media por prioridad: ", media_por_prioridad)

# Por fecha
media_por_fecha_julio = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([7]), 'analisisVulnerabilidades'].mean()
print("Media por fecha (Julio): ", media_por_fecha_julio)
media_por_fecha_agosto = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([8]), 'analisisVulnerabilidades'].mean()
print("Media por fecha (Agosto): ", media_por_fecha_agosto)


#############
# APARTADO E#
#############
# Por prioridad:
varianza_por_prioridad = alerts_devices.groupby('prioridad')['analisisVulnerabilidades'].var(ddof=0)
print("Varianza por prioridad: ", varianza_por_prioridad)

# Por fecha:
varianza_por_fecha_julio = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([7]), 'analisisVulnerabilidades'].var(ddof=0)
print("Varianza por fecha Julio: ", varianza_por_fecha_julio)
varianza_por_fecha_agosto = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([8]), 'analisisVulnerabilidades'].var(ddof=0)
print("Varianza por fecha Agosto: ", varianza_por_fecha_agosto)


#############
# APARTADO F#
#############

# Por prioridad:

max_por_prioridad = alerts_devices.groupby('prioridad')['analisisVulnerabilidades'].max()
print("Máximo por prioridad: ", max_por_prioridad)
min_por_prioridad = alerts_devices.groupby('prioridad')['analisisVulnerabilidades'].min()
print("Mínimo por prioridad: ", min_por_prioridad)

# Máximo por fecha:
max_por_fecha_julio = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([7]), 'analisisVulnerabilidades'].max()
print("Máximo por fecha (Julio): ", max_por_fecha_julio)
max_por_fecha_agosto = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([8]), 'analisisVulnerabilidades'].max()
print("Máximo por fecha (Agosto): ", max_por_fecha_agosto)

# Mínimo por fecha:
min_por_fecha_julio = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([7]), 'analisisVulnerabilidades'].min()
print("Mínimo por fecha (Julio): ", min_por_fecha_julio)
min_por_fecha_agosto = alerts_devices.loc[alerts_devices['timestamp'].dt.month.isin([8]), 'analisisVulnerabilidades'].min()
print("Mínimo por fecha (Agosto): ", min_por_fecha_agosto)

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
# APARTADO B#
#############

alertastas_tiempo_df = df_alerts.groupby('timestamp')['timestamp'].count().reset_index(name='numero_alertas')
alertastas_tiempo_df['timestamp'] = pd.to_datetime(alertastas_tiempo_df['timestamp'])
alertastas_tiempo_df = alertastas_tiempo_df.set_index('timestamp')
alertas_por_dia = alertastas_tiempo_df.resample('D').sum()
plt.plot(alertas_por_dia.index, alertas_por_dia.values)
plt.xlabel('Fecha')
plt.ylabel('Número de alertas')
plt.title('Alertas en el tiempo')
plt.xticks( rotation=30, ha="right", rotation_mode="anchor")
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

dispositivos_vulnerables = pd.read_sql_query("SELECT id, SUM(analisisServiviosInseguros + analisisVulnerabilidades) as numero_vulnerabilidades FROM DEVICES GROUP BY id ORDER BY numero_vulnerabilidades ",con)
vulnerabilidades = dispositivos_vulnerables['numero_vulnerabilidades'].tolist()
etiquetas = dispositivos_vulnerables['id'].tolist()
plt.pie(vulnerabilidades, labels=etiquetas, colors=['red', 'blue', 'pink', 'green', 'yellow', 'purple', 'gray'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Dispositivos más Vulnerables')
plt.show()

#############
# APARTADO E#
#############

openPorts = pd.read_sql_query("SELECT analisisPuertosAbiertos as puertosAbiertos from devices", con)
openPorts.replace(to_replace=["NULL"], value=np.nan, inplace=True)
# Obtener el número de puertos abiertos en cada registro
openPorts['num_puertos'] = openPorts['puertosAbiertos'].fillna('').apply(lambda x: len(re.findall(r'\d+', str(x))))
media_puertos_abiertos = openPorts['num_puertos'].mean()
servicios_inseguros = sum(df_devices['analisisServiviosInseguros'])
servicios = sum(df_devices['analisisServicios'])

puertos_servicios_inseguros = int((media_puertos_abiertos/servicios_inseguros)*100)
puertos_servicios = int((media_puertos_abiertos/servicios)*100)

porcentajes = ['Media Puertos ServiciosInseguros', 'Media Puertos Servicios']
valores = [puertos_servicios_inseguros, puertos_servicios]
plt.bar(porcentajes, valores, color=['red', 'blue'])
plt.ylabel('Valores')
plt.title('Comparación de porcentajes')
plt.show()
