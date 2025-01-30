"""
This is Product Sales Forecasting System

To create and activate virtual environment run following codes in terminal
1. run the flask app with command `flask --app app run` from terminal

"""
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle

# TODO 1: Read all files into Pandas dataframe format
train = pd.read_csv('database/train_processed.csv')
test = pd.read_csv('database/test_processed.csv')
exog_train = pd.read_csv('database/exog_train.csv')
exog_test = pd.read_csv('database/exog_test.csv')

overall_order = train.groupby(level=0).agg({'Order':'sum'})
id_wise_order = pd.crosstab(index=train.index, columns=train.Store_id, values =train.Order, aggfunc='sum')
store_type_wise_order = pd.crosstab(index=train.index, columns=train.Store_Type, values =train.Order, aggfunc='sum')
location_wise_order = pd.crosstab(index=train.index, columns=train.Location_Type, values =train.Order, aggfunc='sum')
region_wise_order = pd.crosstab(index=train.index, columns=train.Region_Code, values =train.Order, aggfunc='sum')

overall_sales = train.groupby(level=0).agg({'Order':'sum'})
id_wise_sales = pd.crosstab(index=train.index, columns=train.Store_id, values =train.Sales, aggfunc='sum')
store_type_wise_sales = pd.crosstab(index=train.index, columns=train.Store_Type, values =train.Sales, aggfunc='sum')
location_wise_sales = pd.crosstab(index=train.index, columns=train.Location_Type, values =train.Sales, aggfunc='sum')
region_wise_sales = pd.crosstab(index=train.index, columns=train.Region_Code, values =train.Sales, aggfunc='sum')

# TODO 2 Configure Flask App
app = Flask(__name__)

# create end points
# Welcome point
@app.route('/') # Homepage
def home():
    return 'Product Sales Forecasting by Ankit Thummar'

# Forecasting
@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    # TODO 3: Return information for GET request
    if request.method=='GET':
        return ('This is Product Sales Forecasting System.\n'
                'Send POST request to get forecasting.\n'
                'JSON Format: {"For":"<All, StoreID, StoreType, Location, Region>",\n'
                '              "SubCategory":"<As per selection in For>",\n'
                '              "ForecastType":"<Sales, Order>",\n'
                '              "n_steps":<integer between 1 and 50>}')
    # TODO 4: Return final result for POST request
    if request.method == 'POST':

        # Function to make Forecasting
        def forecasting(category:str, sub:str, typ:str, n:int):
            """
            :type category: str Any one from (All, StoreID, Location, Region)
            :type sub: str (As per selection of main_category)
            :type typ: str Any one from (Sales, Order)
            :type n: integer
            """
            pkl_file = category + sub + typ + ".pkl"
            with open(pkl_file, 'rb') as file:
                model = pickle.load(file)
            result = model.forecast(n_steps=n, exog=exog_test)
            return result

        # Fetch Query point
        main_category = request.get_json()['For']
        sub_category = request.get_json()['SubCategory']
        forecast_type = request.get_json()['ForecastType']
        n_steps = request.get_json()['n_steps']
        output = forecasting(main_category, sub_category, forecast_type, n_steps)
        return jsonify({'Forecast':output})