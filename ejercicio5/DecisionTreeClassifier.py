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

with open(r'..\Data\devices_IA_clases.json') as f:
    train_data = json.load(f)
with open(r'..\Data\devices_IA_predecir_v2.json') as f:
    test_data = json.load(f)

emails_click = []
phishing_recibidos = []
vulnerable = []
prob_click = []

for line in user_info['usuarios']:
    phishing_recibidos.append(line['emails_phishing_recibidos'])
    emails_click.append(line['emails_phishing_clicados'])
    vulnerable.append(line['vulnerable'])
    if line['emails_phishing_recibidos'] != 0:
        prob_click.append(line['emails_phishing_clicados'] / line['emails_phishing_recibidos'])
    else:
        prob_click.append(0)

user_X = pd.DataFrame({'phishing_recibidos': phishing_recibidos, 'emails_click': emails_click})
user_Y = pd.DataFrame({'vulnerable': vulnerable})

user_X_train = user_X[:20]
usuario_X_test = user_X[20:]
user_X_test = prob_click[20:]
user_X_train = user_X_train.to_numpy().tolist()
usuario_X_test = usuario_X_test.to_numpy().tolist()

user_Y_train = user_Y[:20]
user_Y_test = user_Y[20:]

user_Y_train = user_Y_train.to_numpy().tolist()

clf = tree.DecisionTreeClassifier()
clf = clf.fit(user_X_train, user_Y_train)

user_Y_pred = clf.predict(usuario_X_test)
print("Accuracy Decision Tree: %.2f" % accuracy_score(user_Y_test, user_Y_pred))

# Print plot
dot_data = tree.export_graphviz(clf)
graph = graphviz.Source(dot_data)
graph.render("machine_learning/tree_graph_render")
dot_data = tree.export_graphviz(clf,
                                feature_names=['email recibido', 'email click'],
                                class_names=['No vulnerable', 'Vulnerable'],
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
tree_route = os.getcwd() + 'machine_learning/tree.gv'
if platform == 'win32':
    tree_route = tree_route.replace('/', '\\')
graph.render(tree_route, view=True)
