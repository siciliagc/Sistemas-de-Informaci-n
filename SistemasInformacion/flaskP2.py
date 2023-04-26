import json

from flask import Flask, render_template
import re
import sqlite3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import nan
import plotly.express as px
import plotly
app = Flask(__name__)

@app.route('/')
def index():
    con = sqlite3.connect('ETL_system.db')
    cur = con.cursor()
    df_alerts = pd.read_sql_query("SELECT * from alerts", con)

    ip_mas_problematicas_df = df_alerts[df_alerts['prioridad'] == 1]
    ip_mas_problematicas_df = ip_mas_problematicas_df.groupby('origen')['sid'].count().reset_index(
        name='numero_alertas')
    ip_mas_problematicas_df.sort_values(by=['numero_alertas'], ascending=False, inplace=True)
    ip_mas_problematicas_df.head(10)
    fig = px.bar(ip_mas_problematicas_df.head(10), x='origen', y='numero_alertas', title='Top 10 direcciones IPs más problemáticas', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.debug = True
    app.run()
