from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load saved scaler, PCA, and model
scaler = joblib.load('models/scaler.pkl')
pca = joblib.load('models/pca.pkl')
kmeans = joblib.load('models/kmeans_model.pkl')

# Feature order expected by the model
feature_order = ['Annual_Income', 'Spending_Score__1_100', 'Age', 'Profession', 'Work_Experience', 'Family_Size']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Extract features in correct order
        features = [data.get(feat, 0) for feat in feature_order]
        features_array = np.array(features).reshape(1, -1)
        # Scale and apply PCA
        scaled = scaler.transform(features_array)
        pca_features = pca.transform(scaled)
        # Predict cluster
        cluster_label = kmeans.predict(pca_features)[0]
        # Map cluster to segment name
        centers = kmeans.cluster_centers_
        segment_order = centers.sum(axis=1).argsort()
        segment_names = ['Low Value', 'Medium Value', 'High Value']
        segment_map = {segment_order[i]: segment_names[i] for i in range(len(segment_order))}
        segment = segment_map.get(cluster_label, 'Unknown')
        return jsonify({'segment': segment})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
