"""
This is Product Sales Forecasting System

To create and activate virtual environment run following codes in terminal
1. run the flask app with command `flask --app app.py run` from terminal

"""
from flask import Flask, request, jsonify, render_template
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import pickle

# TODO 1: Read all files into Pandas dataframe format
X_test_exog = pd.read_pickle('database/X_test_exog.pkl')

# Data for SubCategories based on Main Category selection
SUB_CATEGORIES = {
    "All": ['All'],
    "StoreID": [i for i in range(1,367)],
    "StoreType": ["S1", "S2", "S3", "S4"],
    "Location": ["L1", "L2", "L3", "L4", "L5"],
    "Region": ["R1", "R2", "R3", "R4"]
}

# TODO 2 Configure Flask App
app = Flask(__name__)

# create end points
# Welcome point
@app.route('/') # Homepage
def home():
    return render_template('home.html')

@app.route('/get_subcategories')
def sub_categories():
    """Returns subcategories based on the selected main category."""
    main_category = request.args.get("main_category")
    subcategories = SUB_CATEGORIES.get(main_category, [])
    return jsonify(subcategories)

# Forecasting
@app.route('/submit', methods=['GET', 'POST'])
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
            # Define model pickle file path and load the model
            pkl_file = 'models/' + sub.lower() + '_' + typ.lower() + ".pkl"
            with open(pkl_file, 'rb') as file:
                model = pickle.load(file)

            # Define database pickle file path and load data
            split_at = 413
            df = pd.read_pickle('database/'+typ.lower()+'.pkl')[[sub]]
            test = df.iloc[split_at:n+split_at]
            exog = pd.read_pickle('database/X_test_exog.pkl')[:n]
            df = df.iloc[split_at-10:split_at]
            test['pred'] = model.forecast(steps=n, exog=exog)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df[sub], name='Train values'))
            fig.add_trace(go.Scatter(x=test.index, y=test[sub], name='Test values'))
            fig.add_trace(go.Scatter(x=test.index, y=test['pred'], name='Forecasting'))
            fig.update_layout(title_text=f'Forecasting of {typ} for {sub}',
                              title_x=0.5,title_y=0.85, legend_x=0)
            return pio.to_json(fig)

        # Fetch Query point
        main_category = request.get_json()['MainCategory']
        sub_category = request.get_json()['SubCategory']
        n_steps = request.get_json()['n_steps']

        order_forecast = forecasting(main_category, sub_category, 'order', n_steps)
        sales_forecast = forecasting(main_category, sub_category, 'sales', n_steps)
        return jsonify({'order':order_forecast, 'sales':sales_forecast})