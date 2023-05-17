import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
from tqdm import tqdm
from time import sleep

# Load dataset:
with open(r'..\Data\devices_IA_clases.json') as f:
    train_data = json.load(f)
with open(r'..\Data\devices_IA_predecir_v2.json') as f:
    test_data = json.load(f)


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

# Split the data into training and testing sets
# train_X, test_X, train_y, test_y = train_test_split(train_X, train_y, test_size=0.2, random_state=42)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(train_X, train_y)

# Make predictions using the testing set
test_y_pred = regr.predict(test_X)

# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(test_y, test_y_pred))
print(str(test_X))
print(str(test_y))
# Plot outputs
for j in tqdm(range(1)):
    sleep(0.2)
plt.scatter(test_X, test_y, color="black")
plt.plot(test_X, test_y_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()
