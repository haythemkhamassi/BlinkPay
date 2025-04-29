from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Load the saved SARIMAX model
with open('../models/sarimax_model.pkl', 'rb') as f:
    model_fit = pickle.load(f)

# Define the exogenous variable names expected by the model
# This should match the columns used in training except 'Revenu' and 'DateFK'
EXOG_VARS = [
    'Valeur_des_Actifs',
    'Amortissement_Cumule',
    'Cout_de_Maintenance',
    'Investissement_dans_les_Actifs',
    'Quantity'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Validate input keys
        if not all(var in data for var in EXOG_VARS):
            return jsonify({'error': f'Missing one or more required exogenous variables: {EXOG_VARS}'}), 400

        # Create DataFrame for exogenous variables
        exog_input = pd.DataFrame([data], columns=EXOG_VARS)

        # Convert columns to numeric, coerce errors to NaN
        exog_input = exog_input.apply(pd.to_numeric, errors='coerce')

        # Check for NaNs after conversion
        if exog_input.isnull().any().any():
            return jsonify({'error': 'Invalid input values, could not convert to numeric.'}), 400

        # Debug: print input and forecast
        print("Exogenous input for prediction:", exog_input)

        # Forecast one step ahead using the model
        forecast = model_fit.forecast(steps=1, exog=exog_input)

        print("Forecasted value:", forecast.iloc[0])

        # Return the forecasted value
        return jsonify({'forecast': float(forecast.iloc[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
