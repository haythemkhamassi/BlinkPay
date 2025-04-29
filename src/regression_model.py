import pyodbc
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def load_data():
    server = 'DESKTOP-D9RLU4B'
    database = 'DWH'
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'
    )
    query = """
    SELECT ProductID, Quantity, UnitPrice, TotalPrice
    FROM Dim_Facture
    """
    try:
        with pyodbc.connect(connection_string) as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error loading data:", e)
        return None

def preprocess_data(df):
    # If ProductID is categorical, encode it
    if df['ProductID'].dtype == 'object':
        df = pd.get_dummies(df, columns=['ProductID'], drop_first=True)
    return df

def train_model(df):
    X = df.drop('TotalPrice', axis=1)
    y = df['TotalPrice']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R^2 Score: {r2:.2f}")

    # Save the model and columns for later use
    joblib.dump(model, 'models/linear_regression_model.joblib')
    joblib.dump(X.columns.tolist(), 'models/model_columns.joblib')

def main():
    df = load_data()
    if df is not None:
        df = preprocess_data(df)
        train_model(df)

if __name__ == "__main__":
    main()
