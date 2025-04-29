import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from connect_ssms import connect_to_ssms, fetch_dim_product_data
import joblib

def preprocess_data(df):
    # Drop rows with missing target
    df = df.dropna(subset=['Category'])
    # Fill missing values in features with mode or median
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    # Encode categorical features using one-hot encoding except target
    X = df.drop('Category', axis=1)
    X = pd.get_dummies(X, drop_first=True)
    y = df['Category']
    return X, y

def train_random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    # Save the trained model
    joblib.dump(clf, 'models/random_forest_model.joblib')
    print("Model saved to models/random_forest_model.joblib")

if __name__ == "__main__":
    conn = connect_to_ssms()
    if conn:
        df = fetch_dim_product_data(conn)
        if df is not None:
            X, y = preprocess_data(df)
            train_random_forest(X, y)
        conn.close()
