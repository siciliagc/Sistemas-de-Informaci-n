import re
import sqlite3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import nan
import plotly.express as px

con = sqlite3.connect('ETL_system.db')
cur = con.cursor()
df_alerts = pd.read_sql_query("SELECT * from alerts", con)
df_devices = pd.read_sql_query("SELECT * from devices", con)

dispositivos_por_peligrosidad_df = df_devices
print(dispositivos_por_peligrosidad_df['analisisServiviosInseguros'])
print(dispositivos_por_peligrosidad_df['analisisServicios'])
dispositivos_por_peligrosidad_df['ip_peligrosa'] = df_devices['analisisServiviosInseguros'] / df_devices[
    'analisisServicios']
print(dispositivos_por_peligrosidad_df['ip_peligrosa'])
dispositivos_peligrosos_df = dispositivos_por_peligrosidad_df[
    dispositivos_por_peligrosidad_df['ip_peligrosa'] > 0.330000]
dispositivos_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
dispositivos_peligrosos_df.head(3)
etiquetas = dispositivos_peligrosos_df['id'].tolist()
peligrosos = dispositivos_peligrosos_df['ip_peligrosa'].tolist()
# dispositivos_peligrosos_df.head(3).plot(title='Top 3 direcciones IPs más problemáticas', kind="pie", x="id", y="ip_peligrosa")
# plt.xticks(rotation=30, ha="right", rotation_mode="anchor")
plt.pie(peligrosos, labels=etiquetas, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Top 3 Dispositivos más Peligrosos')
plt.show()

"""dispositivos_NO_peligrosos_df = dispositivos_por_peligrosidad_df[
    dispositivos_por_peligrosidad_df['ip_peligrosa'] < 0.330000]
dispositivos_NO_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
dispositivos_peligrosos_df.head(3)
etiquetas = dispositivos_NO_peligrosos_df['id'].tolist()
peligrosos = dispositivos_NO_peligrosos_df['ip_peligrosa'].tolist()
plt.pie(peligrosos, labels=etiquetas, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Dispositivos NO Peligrosos')
plt.show()"""
