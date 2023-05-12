import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from subprocess import call

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

# Entrenamos el Random Forest:
clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
clf.fit(train_X, train_y)

# Hacemos predicciones:

y_pred = clf.predict(test_X)

for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file=f'tree_{i}.dot',
                    feature_names=['servicios_inseguros / servicios'],
                    class_names=['No peligroso', 'Peligroso'],
                    rounded=True,
                    proportion=False,
                    precision=2,
                    filled=True)
    call(['dot', '-Tpng', f'tree_{i}.dot', '-o', f'tree_{i}.png', '-Gdpi=600'])
