import json
from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.express as px
import plotly
import requests
import datetime

app = Flask(__name__)

con = sqlite3.connect('ETL_system.db')
cur = con.cursor()
df_alerts = pd.read_sql_query("SELECT * from alerts", con)
devices_df = pd.read_sql_query(
    "SELECT id, SUM(analisisServiviosInseguros + analisisVulnerabilidades) as numero_vulnerabilidades FROM DEVICES GROUP BY id ORDER BY numero_vulnerabilidades ",
    con)

@app.route('/')
def index():
    quantityIP = 10
    quantityDevices = 5
    # Get the JSON data for the initial graph
    graphIPJSON = graphIP(quantityIP)
    graphDevicesJSON = graphDevices(quantityDevices)
    vulnerabilityJSON = api()
    return render_template('index.html', graphIPJSON=graphIPJSON, quantityIP=quantityIP,
                           graphDevicesJSON=graphDevicesJSON, quantityDevices=quantityDevices, vulnerabilities=vulnerabilityJSON)


@app.route('/graphIP/<int:quantity>')
def graphIP(quantity):
    ip_mas_problematicas_df = df_alerts[df_alerts['prioridad'] == 1]
    ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(
        name='numero_alertas')
    ip_mas_problematicas_df.sort_values(by=['numero_alertas'], ascending=False, inplace=True)

    fig = px.bar(ip_mas_problematicas_df.head(quantity), x='origen', y='numero_alertas', barmode='group',
                 labels=dict(origen="IP", numero_alertas="Número de alertas"))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/graphDevices/<int:quantity>')
def graphDevices(quantity):
    dispositivos_vulnerables_df = devices_df.groupby('id')['numero_vulnerabilidades'].sum().reset_index(
        name='numero_vulnerabilidades')
    dispositivos_vulnerables_df.sort_values(by=['numero_vulnerabilidades'], ascending=False, inplace=True)
    fig = px.bar(dispositivos_vulnerables_df.head(quantity), x='id', y='numero_vulnerabilidades', barmode='group',
                 labels=dict(id="Dispositivo", numero_vulnerabilidades="Número de vulnerabilidades"))
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def api():
    # Hacer una solicitud a la API de cve-search para obtener las últimas 30 vulnerabilidades
    response = requests.get("https://cve.circl.lu/api/last")

    # Verificar que la solicitud se haya realizado con éxito (código de estado 200)
    if response.status_code == 200:
        # Obtener la respuesta en formato JSON
        data = response.json()
        # Ordenar los resultados por fecha de publicación (más reciente primero)
        data_sorted = sorted(data, key=lambda x: x['Published'], reverse=True)
        # Tomar solo los 10 primeros resultados
        last_10_data = data_sorted[:10]
        # Almacenar los datos en una lista de diccionarios
        vulnerabilities = []
        for i in range(10):
            vulnerability = {}
            vulnerability["id"] = last_10_data[i]["id"]
            vulnerability["summary"] = last_10_data[i]["summary"]
            # Reformatear la fecha y agregarla al diccionario
            fecha_publicacion = datetime.datetime.fromisoformat(last_10_data[i]["Published"])
            vulnerability["fecha_publicacion"] = fecha_publicacion.strftime('%d-%m-%Y %H:%M')
            vulnerability["url"] = f"https://cve.circl.lu/cve/{last_10_data[i]['id']}"
            vulnerabilities.append(vulnerability)
        return vulnerabilities

if __name__ == '__main__':
    app.debug = True
    app.run()

def getApp():
    return app
