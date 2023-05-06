# -*- coding: utf-8 -*-
"""smart-diet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lk2IrI-PhMfYAohmh8B3zLpZxQ5XNj8y
"""

!pip install pulp

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from pulp import * 
import seaborn as sns

data = pd.read_csv('/content/drive/MyDrive/datasets/nutrition.csv').drop('Unnamed: 0',axis=1)
data.head()

data = data[['name','serving_size','calories','carbohydrate','total_fat','protein']]

data = data.drop('serving_size',axis=1)

data.info()

data['carbohydrate'] = np.array([data['carbohydrate'].tolist()[i].split(' ') for i in range(len(data))])[:,0].astype('float')
data['protein'] = np.array([data['protein'].tolist()[i].split(' ') for i in range(len(data))])[:,0].astype('float')
data['total_fat'] = np.array([data['total_fat'].tolist()[i].split('g') for i in range(len(data))])[:,0].astype('float')

data['total_fat']

shuffled_data = data.sample(frac=1).reset_index().drop('index',axis=1)

split_data_loc = np.linspace(0,len(shuffled_data),8).astype(int)

shuffled_data.loc[split_data_loc[0]:split_data_loc[1]]

def build_nutritional_values(kg,calories):
    protein_calories = kg*4
    res_calories = calories-protein_calories
    carb_calories = calories/2.
    fat_calories = calories-carb_calories-protein_calories
    res = {'Protein Calories':protein_calories,'Carbohydrates Calories':carb_calories,'Fat Calories':fat_calories}
    return res

def extract_gram(table):
    protein_grams = table['Protein Calories']/4.
    carbs_grams = table['Carbohydrates Calories']/4.
    fat_grams = table['Fat Calories']/9.
    res = {'Protein Grams':protein_grams, 'Carbohydrates Grams':carbs_grams,'Fat Grams':fat_grams}
    return res

print(build_nutritional_values(70,1500))

print(extract_gram(build_nutritional_values(70,1500)))

days_data = random_dataset()
def model(day,kg,calories):
    G = extract_gram(build_nutritional_values(kg,calories))
    E = G['Carbohydrates Grams']
    F = G['Fat Grams']
    P = G['Protein Grams']
    day_data = days_data[day]
    day_data = day_data[day_data.calories!=0]
    food = day_data.name.tolist()
    c  = day_data.calories.tolist()
    x  = pulp.LpVariable.dicts( "x", indices = food, lowBound=0, upBound=1.5, cat='Continuous', indexStart=[] )
    e = day_data.carbohydrate.tolist()
    f = day_data.total_fat.tolist()
    p = day_data.protein.tolist()
    prob  = pulp.LpProblem( "Diet", LpMinimize )
    prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(food))]  )
    prob += pulp.lpSum( [x[food[i]]*e[i] for i in range(len(x)) ] )>=E
    prob += pulp.lpSum( [x[food[i]]*f[i] for i in range(len(x)) ] )>=F
    prob += pulp.lpSum( [x[food[i]]*p[i] for i in range(len(x)) ] )>=P
    prob.solve()
    variables = []
    values = []
    for v in prob.variables():
        variable = v.name
        value = v.varValue
        variables.append(variable)
        values.append(value)
    values = np.array(values).round(2).astype(float)
    sol = pd.DataFrame(np.array([food,values]).T, columns = ['Food','Quantity'])
    sol['Quantity'] = sol.Quantity.astype(float)
    return sol