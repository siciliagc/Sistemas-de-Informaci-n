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

def dispositivos_peligrosos():
    dispositivos_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] >= 0.33]
    dispositivos_peligrosos_df.dropna(inplace=True)
    dispositivos_peligrosos_df['ip_peligrosa'] = (dispositivos_peligrosos_df['analisisServiviosInseguros'] /
                                                  dispositivos_peligrosos_df['analisisServicios']) * 100
    dispositivos_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
    dispositivos_peligrosos_df.head(3)
    fig1 = px.pie(dispositivos_peligrosos_df.head(2), values='ip_peligrosa', names='id',
                  title='Pie Chart of IP Peligrosa by ID',
                  hover_data=['ip_peligrosa'],
                  labels={'ip_peligrosa': 'IP Peligrosa'},
                  template='seaborn'
                  )

    fig1.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    fig1.write_html('plot1.html')

def dispositivos_no_peligrosos():
    dispositivos_no_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] < 0.33]
    dispositivos_no_peligrosos_df.dropna(inplace=True)
    dispositivos_no_peligrosos_df['ip_segura'] = (1 - (dispositivos_no_peligrosos_df['analisisServiviosInseguros'] /
                                                       dispositivos_no_peligrosos_df['analisisServicios'])) * 100
    dispositivos_no_peligrosos_df.sort_values(by=['ip_segura'], ascending=False, inplace=True)
    dispositivos_no_peligrosos_df.head(3)
    fig2 = px.pie(dispositivos_no_peligrosos_df, values='ip_segura', names='id',
                  title='Pie Chart of IP Segura by ID',
                  hover_data=['ip_segura'],
                  labels={'ip_segura': 'IP Segura'},
                  template='seaborn'
                  )

    fig2.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    fig2.write_html('plot2.html')


def total_dispositivos():
    dispositivos_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] >= 0.33]
    dispositivos_peligrosos_df.dropna(inplace=True)
    dispositivos_peligrosos_df['ip_peligrosa'] = (dispositivos_peligrosos_df['analisisServiviosInseguros'] /
                                                  dispositivos_peligrosos_df['analisisServicios']) * 100
    dispositivos_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
    dispositivos_no_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] < 0.33]
    dispositivos_no_peligrosos_df.dropna(inplace=True)
    dispositivos_no_peligrosos_df['ip_segura'] = (1 - (dispositivos_no_peligrosos_df['analisisServiviosInseguros'] /
                                                       dispositivos_no_peligrosos_df['analisisServicios'])) * 100
    dispositivos_no_peligrosos_df.sort_values(by=['ip_segura'], ascending=False, inplace=True)
    secure_services_df = dispositivos_no_peligrosos_df[['id', 'ip_segura']]
    secure_services_df['Status'] = 'Secure'
    unsecure_services_df = dispositivos_peligrosos_df[['id', 'ip_peligrosa']]
    unsecure_services_df['Status'] = 'Unsecure'

    # Rename the columns
    secure_services_df = secure_services_df.rename(columns={'ip_segura': 'ip_security'})
    unsecure_services_df = unsecure_services_df.rename(columns={'ip_peligrosa': 'ip_security'})

    combined_df = pd.concat([secure_services_df, unsecure_services_df], ignore_index=True)

    # Create the sunburst plot using Plotly Express
    fig3 = px.sunburst(combined_df, path=['Status', 'id'], values='ip_security', color='Status', branchvalues='total')

    fig3.update_traces(
        textinfo='label+percent entry',
        hovertemplate='<b>%{id}</b><br>Status: %{label}<br>Value: %{value}'
    )

    fig3.update_layout(
        title='IP Security Status',
        height=600
    )

    fig3.write_html('plot3.html')


