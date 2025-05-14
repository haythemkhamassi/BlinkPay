from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

# Initialisation de l'application
app = Flask(__name__)
CORS(app)

# === Chargement des modèles ===
try:
    regression_model = joblib.load('regression_model.pkl')
    print("✅ Modèle de régression chargé")
except Exception as e:
    print(f"❌ Erreur modèle régression : {e}")
    regression_model = None

try:
    clustering_model = joblib.load('clustering_model.pkl')
    clustering_scaler = joblib.load('clustering_scaler.pkl')
    print("✅ Modèle de clustering chargé")
except Exception as e:
    print(f"❌ Erreur clustering : {e}")
    clustering_model = None
    clustering_scaler = None

try:
    prophet_model = joblib.load('prophet_model.pkl')
    print("✅ Modèle Prophet chargé :", prophet_model)
except Exception as e:
    print("❌ Erreur chargement Prophet :", e)
    prophet_model = None

try:
    classification_model = joblib.load('model.pkl')  # nom de ton modèle sauvegardé
    print("✅ Modèle de classification chargé")
except Exception as e:
    print("❌ Erreur modèle classification :", e)
    classification_model = None

# === Route 1 : Régression ===
@app.route('/predict', methods=['POST'])
def predict():
    if regression_model is None:
        return jsonify({'error': 'Modèle de régression non disponible'}), 500
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        prediction = regression_model.predict(input_df)[0]
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Route 2 : Clustering ===
@app.route('/predict-cluster', methods=['POST'])
def predict_cluster():
    if clustering_model is None or clustering_scaler is None:
        return jsonify({'error': 'Modèle de clustering non disponible'}), 500
    try:
        data = request.get_json()
        expected_fields = ['Gender', 'Age', 'Annual_Income', 'Spending_Score__1_100', 'Work_Experience', 'Family_Size']
        for field in expected_fields:
            if field not in data:
                return jsonify({'error': f"Champ manquant : {field}"}), 400

        input_df = pd.DataFrame([data])
        input_scaled = clustering_scaler.transform(input_df)
        cluster = clustering_model.predict(input_scaled)[0]

        return jsonify({'cluster': int(cluster)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Route 3 : Série temporelle Prophet ===
@app.route('/predict-timeseries', methods=['GET'])
def predict_timeseries_route():
    try:
        if prophet_model is None:
            return jsonify({'error': 'Modèle Prophet non disponible'}), 500

        periods = int(request.args.get('days', 30))
        future = prophet_model.make_future_dataframe(periods=periods)
        forecast = prophet_model.predict(future)
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)

        return jsonify({'forecast': result.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Route 4 : Classification (Fiabilité fournisseur) ===
@app.route('/predict-fournisseur', methods=['POST'])
def predict_fournisseur():
    if classification_model is None:
        return jsonify({'error': 'Modèle de classification non disponible'}), 500
    try:
        data = request.get_json()
        expected_fields = ['NbCommandes', 'MontantTotal', 'DelaiPaiement', 'TypePaiement_Carte', 'TypePaiement_Espèces', 'TypePaiement_Virement']
        for field in expected_fields:
            if field not in data:
                return jsonify({'error': f"Champ manquant : {field}"}), 400

        input_df = pd.DataFrame([data])
        prediction = classification_model.predict(input_df)[0]
        return jsonify({'fiabilite': int(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Lancement de l'app Flask ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
