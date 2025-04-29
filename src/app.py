from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd

app = Flask(__name__)

# Load the saved model and columns
model = joblib.load('models/linear_regression_model.joblib')
model_columns = joblib.load('models/model_columns.joblib')

def preprocess_input(data):
    # Convert input dict to DataFrame
    input_df = pd.DataFrame([data])
    # Handle ProductID encoding if needed
    if 'ProductID' in model_columns:
        # ProductID is numeric, no encoding needed
        input_df = input_df.reindex(columns=model_columns, fill_value=0)
    else:
        # One-hot encoding for ProductID
        product_id_cols = [col for col in model_columns if col.startswith('ProductID_')]
        for col in product_id_cols:
            input_df[col] = 0
        product_col = f"ProductID_{data.get('ProductID')}"
        if product_col in input_df.columns:
            input_df[product_col] = 1
        input_df = input_df.reindex(columns=model_columns, fill_value=0)
    return input_df

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    if request.method == 'POST':
        try:
            product_id = request.form.get('ProductID')
            quantity = float(request.form.get('Quantity'))
            unit_price = float(request.form.get('UnitPrice'))
            data = {
                'ProductID': product_id,
                'Quantity': quantity,
                'UnitPrice': unit_price
            }
            input_df = preprocess_input(data)
            prediction = model.predict(input_df)[0]
        except Exception as e:
            error = str(e)
    html = """
    <!doctype html>
    <html>
    <head>
        <title>Invoice TotalPrice Prediction</title>
        <style>
            body {
                background-color: #121212;
                color: #d7bde2; /* pastel light pink */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                max-width: 420px;
                background-color: #1e1e1e;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(163, 196, 243, 0.7);
                width: 100%;
                box-sizing: border-box;
                text-align: center;
            }
            h1 {
                color: #a3c4f3; /* pastel light blue */
                font-weight: 700;
                font-size: 2.5rem;
                margin-bottom: 20px;
                text-align: center;
                text-shadow: 0 0 8px #a3c4f3;
            }
            label {
                color: #d7bde2;
                font-weight: 600;
                font-size: 1.1rem;
                display: block;
                margin-bottom: 8px;
            }
            input[type="text"], input[type="number"] {
                background-color: #1e1e1e;
                border: 1px solid #444;
                color: #d7bde2;
                padding: 10px 12px;
                width: 320px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 1rem;
                transition: border-color 0.3s ease;
            }
            input[type="text"]:focus, input[type="number"]:focus {
                border-color: #a3c4f3;
                outline: none;
                box-shadow: 0 0 8px #a3c4f3;
            }
            input[type="submit"] {
                background-color: #a3c4f3;
                color: #121212;
                border: none;
                padding: 12px 28px;
                font-size: 1.2rem;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 700;
                box-shadow: 0 4px 12px rgba(163, 196, 243, 0.6);
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
                display: block;
                margin: 0 auto;
            }
            input[type="submit"]:hover {
                background-color: #8ab0e3;
                box-shadow: 0 6px 16px rgba(138, 176, 227, 0.8);
            }
            h2 {
                color: #a3c4f3;
                margin-top: 25px;
                font-weight: 600;
                font-size: 1.5rem;
                text-shadow: 0 0 6px #a3c4f3;
            }
            h3 {
                color: #f1948a; /* pastel light pink */
                margin-top: 20px;
                font-weight: 600;
                font-size: 1.2rem;
                text-shadow: 0 0 6px #f1948a;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Predict TotalPrice</h1>
            <form method="post">
                <label for="ProductID">ProductID:</label><br>
                <input type="text" id="ProductID" name="ProductID" required><br>
                <label for="Quantity">Quantity:</label><br>
                <input type="number" step="any" id="Quantity" name="Quantity" required><br>
                <label for="UnitPrice">UnitPrice:</label><br>
                <input type="number" step="any" id="UnitPrice" name="UnitPrice" required><br>
                <input type="submit" value="Predict">
            </form>
            {% if prediction is not none %}
                <h2>Predicted TotalPrice: {{ prediction }}</h2>
            {% endif %}
            {% if error %}
                <h3>Error: {{ error }}</h3>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, prediction=prediction, error=error)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        input_df = preprocess_input(data)
        prediction = model.predict(input_df)[0]
        return jsonify({'predicted_TotalPrice': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
