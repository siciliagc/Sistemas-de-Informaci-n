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

ip_mas_problematicas_df = df_alerts[df_alerts['prioridad']==1]
ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(name='numero_alertas')
ip_mas_problematicas_df.sort_values(by=['numero_alertas'],ascending=False, inplace=True)
ip_mas_problematicas_df.head(10).plot(title='Top 10 direcciones IPs más problemáticas', x="origen", y="numero_alertas", kind="bar")
plt.xticks(rotation=30, ha="right", rotation_mode="anchor")
plt.show()