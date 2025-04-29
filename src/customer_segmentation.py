import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sqlserver_connection import connect_to_sql_server, fetch_dim_customer_data
import joblib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load_data():
    conn = connect_to_sql_server()
    if conn:
        rows = fetch_dim_customer_data(conn)
        conn.close()
        if rows:
            df = pd.DataFrame.from_records(rows, columns=[
                'ID_Customer', 'Gender', 'Age', 'Annual_Income', 'Spending_Score__1_100',
                'Profession', 'Work_Experience', 'Family_Size'
            ])
            return df
    return pd.DataFrame()

def preprocess_data(df):
    df = df.dropna(subset=['Annual_Income', 'Spending_Score__1_100'])
    df['Gender'] = df['Gender'].astype('category').cat.codes
    df['Profession'] = df['Profession'].astype('category').cat.codes
    return df

def feature_engineering(df):
    df['Value_Score'] = (df['Annual_Income'] * df['Spending_Score__1_100']) / 100
    return df

def train_and_save_model(df, n_clusters=3):
    features = ['Annual_Income', 'Spending_Score__1_100', 'Age', 'Profession', 'Work_Experience', 'Family_Size']
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features])

    pca = PCA(n_components=2, random_state=42)
    pca_features = pca.fit_transform(scaled_features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pca_features)

    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(pca, 'models/pca.pkl')
    joblib.dump(kmeans, 'models/kmeans_model.pkl')
    print("Model, scaler, and PCA saved successfully.")

def main():
    df = load_data()
    if df.empty:
        print("No data loaded.")
        return
    df = preprocess_data(df)
    df = feature_engineering(df)
    train_and_save_model(df)

if __name__ == "__main__":
    main()
