import json
import os
from subprocess import call
from sys import platform
import graphviz
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, accuracy_score
from sklearn.tree import export_graphviz

# Cargamos los datos de los dispositivos:

with open(r'..\Data\devices_IA_clases.json') as f:
    train_data = json.load(f)
with open(r'..\Data\devices_IA_predecir_v2.json') as f:
    test_data = json.load(f)

train_X = []
train_y = []

for i in train_data:
    if (i['servicios'] == 0):
        continue
    train_X.append([i['servicios_inseguros'] / i['servicios']])
    train_y.append(i['peligroso'])

test_X = []
test_y = []
for i in test_data:
    if(i['servicios']==0):
        continue
    test_X.append([i['servicios_inseguros']/i['servicios']])
    test_y.append(i['peligroso'])

clf = RandomForestClassifier(max_depth=5, random_state=0, n_estimators=10)
clf.fit(train_X, train_y)

user_Y_pred = clf.predict(test_X)

for i in range(len(clf.estimators_)):
    print(i)
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='tree.dot',
                    feature_names=['servicios_inseguros/servicios'],
                    class_names=['No Peligroso', 'Peligroso'],
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot','-Tpng', 'tree.dot','-o','tree' + str(i) + '.png','-Gdpi=600'])



