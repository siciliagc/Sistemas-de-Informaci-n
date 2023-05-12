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

with open(r'..\Data\devices_IA_clases.json') as f:
    train_data = json.load(f)
with open(r'..\Data\devices_IA_predecir_v2.json') as f:
    test_data = json.load(f)

# Extract the "servicios" feature from the training data
prob_servicios_inseguros = []
servicios_inseguros = []
servicios = []
peligroso = []


# Extract the "servicios" feature from the training data
train_X = [] #[[d['servicios']] for d in train_data]
train_y = []
test_X = []
test_y = []

for i in train_data:
    if(i['servicios']==0):
        continue
    train_X.append([i['servicios_inseguros']/i['servicios']])
    train_y.append(i['peligroso'])

for i in test_data:
    if(i['servicios']==0):
        continue
    test_X.append([i['servicios_inseguros']/i['servicios']])
    test_y.append(i['peligroso'])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_X, train_y)

dot_data = tree.export_graphviz(clf)
graph = graphviz.Source(dot_data)
graph.render("ejercicio5/machine_learning")
dot_data = tree.export_graphviz(clf,
                                feature_names=['servicios'],
                                class_names=['No Peligroso', 'Peligroso'],
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)



