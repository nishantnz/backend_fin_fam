import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import json
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

app = Flask(__name__)

dataset = pd.read_csv('inc_children_data_50.csv')

x = dataset.iloc[:, :1].values
y = dataset.iloc[:, 2].values

for i in range(0, len(x)):
  x[i, 0] = int(x[i, 0].replace(",", ""))
y = y.reshape(len(y), 1)

sc_x = StandardScaler()
sc_y = StandardScaler()
x = sc_x.fit_transform(x)
y = sc_y.fit_transform(y)

regressor = SVR(kernel='rbf')
regressor.fit(x, y)

print("Training completed for Children .......")

x = dataset.iloc[:, 2:].values
y = dataset.iloc[:, 0].values

for i in range(0, len(y)):
    y[i] = int(y[i].replace(",", ""))
y = y.reshape(len(y), 1)
sc_x_1 = StandardScaler()
sc_y_1 = StandardScaler()
x = sc_x_1.fit_transform(x)
y = sc_y_1.fit_transform(y)

regressor = SVR(kernel='rbf')
regressor.fit(x, y)

print("Training Completed for Income.......")


@app.route('/predictChildren', methods=['POST'])
def predictChildren():
    content_type = request.headers.get('Content-Type')
    print("Content type : ", content_type)
    data = json.loads(request.data)

    print(data)
    print("income : ", data['income'])
    
    income = data['income']
    debt = data['debt']
    investment = data['investment']

    fin = income - debt + investment
    chi = math.floor(sc_y.inverse_transform(
        regressor.predict(sc_x.transform([[fin]])).reshape(-1, 1)))
    if chi > 3:
        chi = 3

    return jsonify({'Number of Children': str(chi)})

@app.route('/predictFamily', methods=['POST'])
def predictFamily():

    content_type = request.headers.get('Content-Type')
    print("Content type : ", content_type)
    data = json.loads(request.data)
    print(data)
    print("income : ", data['income'])

    income = data['income']

    dataset = pd.read_csv('fam_fin_plan.csv')
    p = dataset.iloc[:, 6:14].values

    for i in range(3143):
        for j in range(8):
            p[i][j] = p[i][j].replace("$", "")
            p[i][j] = int(p[i][j].replace(",", ""))

    for i in range(3143):
        for j in range(7):
            p[i][j] = (p[i][j]/p[i][7])*100

        """
        p_housing
        p_food
        p_transportation
        p_healthcare
        p_othernecessities
        p_childcare
        p_taxes
        """

    perc = [0]*7
    for i in range(7):
        for j in range(3143):
            perc[i] = perc[i] + p[j][i]
    for i in range(7):
        perc[i] = round(perc[i]/3143)/100
    print(perc)

    plan = [0]*7
    for i in range(7):
        # 60000*12 = 720000, is the cost for the parents which is removed(based on research)
        plan[i] = (income - 720000) * perc[i]

    return jsonify({"Housing": plan[0], "Food": plan[1], "Transportation": plan[2], "Healthcare": plan[3], "Other Necessities": plan[4], "Childcare": plan[5], "Taxes": plan[6]})    

@app.route('/predictIncome', methods=['POST'])
def predictIncome():

    content_type = request.headers.get('Content-Type')
    print("Content type : ", content_type)
    data = json.loads(request.data)
    print(data)
    print("childrens : ", data['childrens'])

    n = data['childrens']

    t = sc_y_1.inverse_transform(regressor.predict(
        sc_x_1.transform([[n]])).reshape(-1, 1))
    tval = t[0][0]

    return jsonify({"Income": tval})


if __name__ == "__main__":
    app.run(debug=True)
