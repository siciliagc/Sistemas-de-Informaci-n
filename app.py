import json
import tempfile
from flask import Flask, render_template, jsonify, make_response
import sqlite3
import pandas as pd
import plotly.express as px
import plotly
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import plotly.io as pio
import os
from flask_weasyprint import HTML, render_pdf
import kaleido
import uuid

app = Flask(__name__)

con = sqlite3.connect('ETL_system.db')
cur = con.cursor()
alerts_df = pd.read_sql_query("SELECT * from alerts", con)
devices_df = pd.read_sql_query(
    "SELECT id, SUM(analisisServiviosInseguros + analisisVulnerabilidades) as numero_vulnerabilidades FROM DEVICES GROUP BY id ORDER BY numero_vulnerabilidades ",
    con)
df_devices = pd.read_sql_query("SELECT * from devices", con)
vulnerabilities = []
last_updated_cve = ""
quantityIP = 10
quantityDevices = 5
quantityDangerous = 3
quantitySecure = 3


@app.route('/')
def index():
    # Get the JSON data for the initial graph
    graphIPJSON = graphIP(quantityIP)
    graphDevicesJSON = graphDevices(quantityDevices)
    graphDangerousJSON = graphDangerous(quantityDangerous)
    graphSecureJSON = graphSecure(quantitySecure)
    graphTotalSecurityJSON = graphTotalSecurity()

    return render_template('index.html', graphIPJSON=graphIPJSON, quantityIP=quantityIP,
                           graphDevicesJSON=graphDevicesJSON, quantityDevices=quantityDevices,
                           graphDangerousJSON=graphDangerousJSON, quantityDangerous=quantityDangerous,
                           graphSecureJSON=graphSecureJSON, quantitySecure=quantitySecure,
                           graphTotalSecurityJSON=graphTotalSecurityJSON,
                           vulnerabilities=vulnerabilities, last_updated_cve=last_updated_cve)


@app.route('/graphIP/<int:quantity>')
def graphIP(quantity):
    global quantityIP
    quantityIP = quantity
    ip_mas_problematicas_df = alerts_df[alerts_df['prioridad'] == 1]
    ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(
        name='numero_alertas')
    ip_mas_problematicas_df.sort_values(by=['numero_alertas'], ascending=False, inplace=True)

    fig = px.bar(ip_mas_problematicas_df.head(quantityIP), x='origen', y='numero_alertas', barmode='group',
                 labels=dict(origen="IP", numero_alertas="Número de alertas"))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/graphDevices/<int:quantity>')
def graphDevices(quantity):
    global quantityDevices
    quantityDevices = quantity
    dispositivos_vulnerables_df = devices_df.groupby('id')['numero_vulnerabilidades'].sum().reset_index(
        name='numero_vulnerabilidades')
    dispositivos_vulnerables_df.sort_values(by=['numero_vulnerabilidades'], ascending=False, inplace=True)
    fig = px.bar(dispositivos_vulnerables_df.head(quantityDevices), x='id', y='numero_vulnerabilidades', barmode='group',
                 labels=dict(id="Dispositivo", numero_vulnerabilidades="Número de vulnerabilidades"))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/graphDangerous/<int:quantity>')
def graphDangerous(quantity):
    global quantityDangerous
    quantityDangerous = quantity
    dispositivos_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] >= 0.33]
    dispositivos_peligrosos_df.dropna(inplace=True)
    dispositivos_peligrosos_df['ip_peligrosa'] = (dispositivos_peligrosos_df['analisisServiviosInseguros'] /
                                                  dispositivos_peligrosos_df['analisisServicios']) * 100
    dispositivos_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
    fig = px.pie(dispositivos_peligrosos_df.head(quantityDangerous), values='ip_peligrosa', names='id',
                  title='El valor asociado a cada dispositivo el es porcentaje de servicios inseguros',
                  hover_data=['ip_peligrosa'],
                  labels={'ip_peligrosa': 'IP Peligrosa'},
                  template='seaborn'
                  )

    fig.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/graphSecure/<int:quantity>')
def graphSecure(quantity):
    global quantitySecure
    quantitySecure = quantity
    dispositivos_no_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] < 0.33]
    dispositivos_no_peligrosos_df.dropna(inplace=True)
    dispositivos_no_peligrosos_df['ip_segura'] = (1 - (dispositivos_no_peligrosos_df['analisisServiviosInseguros'] /
                                                       dispositivos_no_peligrosos_df['analisisServicios'])) * 100
    dispositivos_no_peligrosos_df.sort_values(by=['ip_segura'], ascending=False, inplace=True)
    fig = px.pie(dispositivos_no_peligrosos_df.head(quantitySecure), values='ip_segura', names='id',
                  title='El valor asociado a cada dispositivo el es porcentaje de servicios seguros',
                  hover_data=['ip_segura'],
                  labels={'ip_segura': 'IP Segura'},
                  template='seaborn')

    fig.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def graphTotalSecurity():
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
    fig = px.sunburst(combined_df, path=['Status', 'id'], values='ip_security', color='Status', branchvalues='total')

    fig.update_traces(
        textinfo='label+percent entry',
        hovertemplate='<b>%{id}</b><br>Status: %{label}<br>Value: %{value}'
    )

    fig.update_layout(
        title='IP Security Status',
        height=600
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def vulnerabilities_cve():
    global vulnerabilities
    global last_updated_cve
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
            vulnerability = {"id": last_10_data[i]["id"], "summary": last_10_data[i]["summary"]}
            # Reformatear la fecha y agregarla al diccionario
            fecha_publicacion = datetime.datetime.fromisoformat(last_10_data[i]["Published"])
            vulnerability["fecha_publicacion"] = fecha_publicacion.strftime('%d-%m-%Y %H:%M')
            vulnerability["url"] = f"https://cve.circl.lu/cve/{last_10_data[i]['id']}"
            vulnerabilities.append(vulnerability)
        last_updated_cve = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def graphIPPdf():
    global quantityIP
    ip_mas_problematicas_df = alerts_df[alerts_df['prioridad'] == 1]
    ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(
        name='numero_alertas')
    ip_mas_problematicas_df.sort_values(by=['numero_alertas'], ascending=False, inplace=True)

    fig = px.bar(ip_mas_problematicas_df.head(quantityIP), x='origen', y='numero_alertas', barmode='group',
                 labels=dict(origen="IP", numero_alertas="Número de alertas"))
    # Save the graph as a static image file in the relative directory
    graph_filename = f'graph_{str(uuid.uuid4())[:8]}.png'
    graph_filepath = os.path.join('static', 'assets', 'img', 'graphs', graph_filename)
    pio.write_image(fig, graph_filepath, format='png', engine='kaleido')

    # Return the path to the graph image file
    return graph_filepath

def graphDevicesPdf():
    global quantityDevices
    dispositivos_vulnerables_df = devices_df.groupby('id')['numero_vulnerabilidades'].sum().reset_index(
        name='numero_vulnerabilidades')
    dispositivos_vulnerables_df.sort_values(by=['numero_vulnerabilidades'], ascending=False, inplace=True)
    fig = px.bar(dispositivos_vulnerables_df.head(quantityDevices), x='id', y='numero_vulnerabilidades', barmode='group',
                 labels=dict(id="Dispositivo", numero_vulnerabilidades="Número de vulnerabilidades"))

    # Save the graph as a static image file in the relative directory
    graph_filename = f'graph_{str(uuid.uuid4())[:8]}.png'
    graph_filepath = os.path.join('static', 'assets', 'img', 'graphs', graph_filename)
    pio.write_image(fig, graph_filepath, format='png', engine='kaleido')

    # Return the path to the graph image file
    return graph_filepath

def graphDangerousPdf():
    global quantityDangerous
    dispositivos_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] >= 0.33]
    dispositivos_peligrosos_df.dropna(inplace=True)
    dispositivos_peligrosos_df['ip_peligrosa'] = (dispositivos_peligrosos_df['analisisServiviosInseguros'] /
                                                  dispositivos_peligrosos_df['analisisServicios']) * 100
    dispositivos_peligrosos_df.sort_values(by=['ip_peligrosa'], ascending=False, inplace=True)
    fig = px.pie(dispositivos_peligrosos_df.head(quantityDangerous), values='ip_peligrosa', names='id',
                  title='El valor asociado a cada dispositivo el es porcentaje de servicios inseguros',
                  hover_data=['ip_peligrosa'],
                  labels={'ip_peligrosa': 'IP Peligrosa'},
                  template='seaborn')

    fig.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    # Save the graph as a static image file in the relative directory
    graph_filename = f'graph_{str(uuid.uuid4())[:8]}.png'
    graph_filepath = os.path.join('static', 'assets', 'img', 'graphs', graph_filename)
    pio.write_image(fig, graph_filepath, format='png', engine='kaleido')

    # Return the path to the graph image file
    return graph_filepath

def graphSecurePdf():
    global quantitySecure
    dispositivos_no_peligrosos_df = df_devices.loc[df_devices['analisisServiviosInseguros'] / df_devices[
        'analisisServicios'] < 0.33]
    dispositivos_no_peligrosos_df.dropna(inplace=True)
    dispositivos_no_peligrosos_df['ip_segura'] = (1 - (dispositivos_no_peligrosos_df['analisisServiviosInseguros'] /
                                                       dispositivos_no_peligrosos_df['analisisServicios'])) * 100
    dispositivos_no_peligrosos_df.sort_values(by=['ip_segura'], ascending=False, inplace=True)
    fig = px.pie(dispositivos_no_peligrosos_df.head(quantitySecure), values='ip_segura', names='id',
                  title='El valor asociado a cada dispositivo el es porcentaje de servicios seguros',
                  hover_data=['ip_segura'],
                  labels={'ip_segura': 'IP Segura'},
                  template='seaborn')

    fig.update_traces(texttemplate='%{label}: %{value:.2f}', textposition='inside')
    # Save the graph as a static image file in the relative directory
    graph_filename = f'graph_{str(uuid.uuid4())[:8]}.png'
    graph_filepath = os.path.join('static', 'assets', 'img', 'graphs', graph_filename)
    pio.write_image(fig, graph_filepath, format='png', engine='kaleido')

    # Return the path to the graph image file
    return graph_filepath

def graphTotalSecurityPdf():
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
    fig = px.sunburst(combined_df, path=['Status', 'id'], values='ip_security', color='Status', branchvalues='total')

    fig.update_traces(
        textinfo='label+percent entry',
        hovertemplate='<b>%{id}</b><br>Status: %{label}<br>Value: %{value}'
    )

    fig.update_layout(
        title='IP Security Status',
        height=600
    )
    # Save the graph as a static image file in the relative directory
    graph_filename = f'graph_{str(uuid.uuid4())[:8]}.png'
    graph_filepath = os.path.join('static', 'assets', 'img', 'graphs', graph_filename)
    pio.write_image(fig, graph_filepath, format='png', engine='kaleido')

    # Return the path to the graph image file
    return graph_filepath


@app.route('/pdf')
def pdf():
    vulnerabilities_cve()

    # Generate the graph
    graph1 = graphIPPdf()
    graph2 = graphDevicesPdf()
    graph3 = graphDangerousPdf()
    graph4 = graphSecurePdf()
    graph5 = graphTotalSecurityPdf()

    # Render the HTML template with the vulnerability information
    rendered_html = render_template('pdf.html', vulnerabilities=vulnerabilities, last_updated_cve=last_updated_cve,
                                    graphIP=graph1, quantityIP=quantityIP,
                                    graphDevices=graph2, quantityDevices=quantityDevices,
                                    graphDangerous=graph3, quantityDangerous=quantityDangerous,
                                    graphSecure=graph4, quantitySecure=quantitySecure,
                                    graphTotalSecurity=graph5)

    # Generate the PDF from the rendered HTML using
    pdf_file = render_pdf(HTML(string=rendered_html, base_url='.'))

    # Delete the graphs images files
    if graph1:
        os.remove(graph1)
    if graph2:
        os.remove(graph2)
    if graph3:
        os.remove(graph3)
    if graph4:
        os.remove(graph4)
    if graph5:
        os.remove(graph5)

    # Create a response object with PDF MIME type
    response = make_response(pdf_file)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    return response


@app.route('/api/cve')
def update_cve():
    return jsonify(vulnerabilities, last_updated_cve)


if __name__ == '__main__':
    # Create a scheduler object
    scheduler = BackgroundScheduler()
    # Add a job to the scheduler to update the vulnerabilities every minute
    scheduler.add_job(func=vulnerabilities_cve, trigger='interval', minutes=1)
    # Start the scheduler
    scheduler.start()
    vulnerabilities_cve()
    app.debug = True
    app.run()
