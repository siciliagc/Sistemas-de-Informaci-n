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
from tqdm import tqdm
from time import sleep

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


# Main prog:

train_X = []
train_y = []
test_X = []
test_y = []
id = []

train_path = r'..\devices_IA_clases.json'


load_train_data(train_path,train_X, train_y)

clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
clf.fit(train_X, train_y)
predict = clf.predict(train_X)
print(predict)


for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='tree.dot',
                    feature_names=['servicios', 'servicios_inseguros'],
                    class_names=['No peligroso', 'Peligroso'],
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree' + str(i) + '.png', '-Gdpi=600'])

for j in tqdm(clf.estimators_):
    sleep(0.2)
c = 0
for i in range(len(predict)):
    if predict[i] == 1:
        c += 1
print("Número de dispositivos peligrosos: ", c)
