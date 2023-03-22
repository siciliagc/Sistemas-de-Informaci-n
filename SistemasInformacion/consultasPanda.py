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
def convertArray(columns: List[str]) -> str:
    string_result: str = columns[0]
    for c in range(1, len(columns)):
        string_result = string_result + ", " + columns[c]
    return string_result

def fetch_tables(table: str, columns: str):
    cur.execute("SELECT "+ columns+ "FROM "+ table)
    return cur.fetchall()


def createDataframe(table: str, columns: list[str]):
    return pd.DataFrame(fetch_tables(table, convertArray(columns)), columns=columns)


# Dataframe para devices:
devices_and_none = createDataframe("devices", ["id", "ip", "localizacion", "responsableNombre", "responsableTlfn", "responsableRol", "analisisPuertosAbiertos", "analisisServicios", "analisisServiviosInseguros", "analisisVulnerabilidades"])

# Apartado a: Número de dispositivos (y campos missing o None).



