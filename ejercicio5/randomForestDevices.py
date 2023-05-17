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


#######################
###### LOAD DATA ######
#######################

def load_train_data(data, train_X, train_y):
    with open(data) as f:
        train_data = json.load(f)
        for i in train_data:
            if (i['servicios'] == 0):
                continue
            train_X.append([i['servicios'], i['servicios_inseguros'], ])
            train_y.append(i['peligroso'])


def predict(test_data, tree, test_X):
    with open(test_data) as f:
        test_data = json.load(f)
    id = []
    for i in test_data:
        if (i['servicios'] == 0):
            continue
        test_X.append([i['servicios'], i['servicios_inseguros'], ])
        id.append(i['id'])
    test_y = tree.predict(test_X)
    return test_y, id


# Main prog:

train_X = []
train_y = []
test_X = []
test_y = []
id = []

train_path = r'..\Data\devices_IA_clases.json'
test_path = r'..\Data\devices_IA_predecir_v2.json'

load_train_data(train_path, train_X, train_y)
clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
clf.fit(train_X, train_y)
print(clf.predict(train_X))

for i in range(len(clf.estimators_)):
    print(i)
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='tree.dot',
                    feature_names=['servicios', 'servicios_inseguros'],
                    class_names=['No peligroso', 'Peligroso'],
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree'+str(i)+'.png', '-Gdpi=600'])

test_y, id = predict(test_path, clf, test_X)
count = 0

dispositivos_peligrosos = []
for i in range(len(test_y)):
    if test_y[i] == 1:
        count += 1
        dispositivos_peligrosos.append(id[i])

print("Número de dispositivos peligrosos: ", count)
print("Se muestran a continuación la lista de dispositivos peligrosos: ", end=" ")
print(dispositivos_peligrosos)




