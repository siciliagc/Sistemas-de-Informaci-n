import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import json

# Load dataset:
with open(r'C:\Users\sicil\OneDrive\Documentos\GitHub\Sistemas-de-Informacion\Data\devices_IA_clases.json') as f:
    train = json.load(f)
with open(r'C:\Users\sicil\OneDrive\Documentos\GitHub\Sistemas-de-Informacion\Data\devices_IA_predecir_v2.json') as f:
    test = json.load(f)

df_entrenamiento = pd.DataFrame(train)
df_predecir = pd.DataFrame(test)

X = df_entrenamiento[['servicios_inseguros']]
y = pd.Series(df_entrenamiento['peligroso']).astype(int).apply(lambda x: 1 if x > 0 else 0)

modelo = linear_model.LinearRegression()
modelo.fit(X, y)

plt.scatter(X, y)
plt.plot(X, modelo.predict(X), color='red')
plt.xlabel('Servicios inseguros')
plt.ylabel('Peligroso')
plt.show()

X_predecir = df_predecir[['servicios_inseguros']].astype(int)
predicciones = modelo.predict(X_predecir).round().astype(int)

df_predecir['peligroso'] = pd.Series(predicciones).apply(lambda x: 1 if x > 0 else 0)

num_peligrosos = df_predecir['peligroso'].sum()

predecir_con_predicciones = df_predecir.to_dict(orient='records')
with open(r'C:\Users\sicil\OneDrive\Documentos\GitHub\Sistemas-de-Informacion\Data\devices_IA_predecir_v2.json', 'w') as f:
    json.dump(predecir_con_predicciones, f)
