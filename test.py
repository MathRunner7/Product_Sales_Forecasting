from flask import Flask, request, jsonify, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import numpy as np
import pickle

# TODO 1: Read all files into Pandas dataframe format
train = pd.read_csv('database/train_processed.csv')
test = pd.read_csv('database/test_processed.csv')
exog_train = pd.read_csv('database/exog_train.csv')
exog_test = pd.read_csv('database/exog_test.csv')

X_test_exog = pd.read_csv('database/X_test_exog.csv').set_index('Date')
print(X_test_exog[:10])
n = 10
pkl_file = "models/l2_order.pkl"
with open(pkl_file, 'rb') as file:
    model = pickle.load(file)

print(model.summary())
result = model.forecast(steps=n, exog=X_test_exog[:n])
print(result)