from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the saved model
model = joblib.load('models/random_forest_model.joblib')

def preprocess_input(data):
    # Convert input dict to DataFrame
    df = pd.DataFrame([data])
    # Fill missing values and encode categorical variables as done in training
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    # One-hot encode categorical variables
    df = pd.get_dummies(df, drop_first=True)
    return df

@app.route('/')
def index():
    # Use the fields except Category as input features
    features = ['ProductID', 'SupplierID', 'ProductName', 'Price']
    return render_template('index.html', features=features)

@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        data = request.json
    else:
        # Get form data as dict
        data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        processed_data = preprocess_input(data)
        # Align processed_data columns with model training columns
        model_features = model.feature_names_in_
        for col in model_features:
            if col not in processed_data.columns:
                processed_data[col] = 0
        processed_data = processed_data[model_features]
        prediction = model.predict(processed_data)
        if request.is_json:
            return jsonify({'predicted_category': prediction[0]})
        else:
            features = ['ProductID', 'SupplierID', 'ProductName', 'Price']
            return render_template('index.html', features=features, prediction=prediction[0])
    except Exception as e:
        if request.is_json:
            return jsonify({'error': str(e)}), 500
        else:
            features = ['ProductID', 'SupplierID', 'ProductName', 'Price']
            return render_template('index.html', features=features, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
