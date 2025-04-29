import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from connect_dwh import connect_to_dwh

def load_data():
    conn = connect_to_dwh()
    if conn is None:
        raise Exception("Database connection failed")

    query = """
    SELECT 
        d.FullDate as Date,
        f.FactureFK,
        f.StatementFK,
        f.PaimentFK,
        f.Valeur_des_Actifs,
        f.Amortissement_Cumule,
        f.Cout_de_Maintenance,
        f.Revenu,
        f.Investissement_dans_les_Actifs,
        f.Quantity,
        f.TotalPrice,
        f.Prix_Unitaire
    FROM FactComptabilite f
    JOIN Dim_Date d ON f.DateFK = d.DateID
    ORDER BY d.FullDate
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def prepare_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    # Aggregate duplicates by summing numeric columns
    df = df.groupby('Date').sum().reset_index()
    df = df.sort_values('Date')
    df.set_index('Date', inplace=True)
    # Forward fill missing dates to create continuous time series
    df = df.asfreq('D')
    # Fill missing numeric values with interpolation or zero
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear').fillna(0)
    return df

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pickle

def build_model(df):
    # Split data into train and test sets (e.g., last 20% as test)
    split_idx = int(len(df) * 0.8)
    train, test = df.iloc[:split_idx], df.iloc[split_idx:]

    # Handle case when training set is empty due to small dataset
    if train.empty:
        print("Training set is empty after split. Using entire dataset for training.")
        train = df
        test = df.iloc[0:0]  # empty test set

    # Define exogenous variables as only the 5 numeric columns used in backend and frontend
    exog_vars = [
        'Valeur_des_Actifs',
        'Amortissement_Cumule',
        'Cout_de_Maintenance',
        'Investissement_dans_les_Actifs',
        'Quantity'
    ]

    # Convert exogenous variables to numeric, coerce errors to NaN
    train_exog = train[exog_vars].apply(pd.to_numeric, errors='coerce')
    test_exog = test[exog_vars].apply(pd.to_numeric, errors='coerce')

    # Convert target variable to numeric and drop NaNs
    train_endog = pd.to_numeric(train['Revenu'], errors='coerce').dropna()
    test_endog = pd.to_numeric(test['Revenu'], errors='coerce').dropna()

    # Align exogenous variables with target variable indices
    train_exog = train_exog.loc[train_endog.index]
    test_exog = test_exog.loc[test_endog.index]

    # Drop columns with any NaN values in exogenous variables
    train_exog = train_exog.dropna(axis=1)

    # Drop columns in test_exog that are not in train_exog
    test_exog = test_exog.loc[:, train_exog.columns]

    # Drop columns with zero variance in train_exog
    variance = train_exog.var()
    zero_variance_cols = variance[variance == 0].index
    train_exog = train_exog.drop(columns=zero_variance_cols)
    test_exog = test_exog.drop(columns=zero_variance_cols)

    # Debug prints for shapes
    print(f"train_endog shape: {train_endog.shape}")
    print(f"train_exog shape: {train_exog.shape}")

    # Check if exogenous variables are empty after cleaning
    if train_exog.shape[1] == 0:
        print("No valid exogenous variables available after cleaning. Fitting model without exogenous variables.")

        # Ensure all data are float64 type to avoid dtype object error
        train_endog = train_endog.astype('float64')
        test_endog = test_endog.astype('float64')

        # Using SARIMAX to model Revenu without exogenous variables on train set
        model = SARIMAX(train_endog, order=(1,1,1), seasonal_order=(0,0,0,0))
        model_fit = model.fit(disp=False)
        print(model_fit.summary())

        # Save the model to disk
    with open('../models/sarimax_model.pkl', 'wb') as f:
        pickle.dump(model_fit, f)

        # Forecast on test set without exogenous variables
        if len(test_endog) > 0:
            forecast = model_fit.get_forecast(steps=len(test_endog))
            forecast_values = forecast.predicted_mean

            # Calculate error metrics
            mae = mean_absolute_error(test_endog, forecast_values)
            mse = mean_squared_error(test_endog, forecast_values)
            rmse = np.sqrt(mse)

            print(f"Mean Absolute Error (MAE): {mae}")
            print(f"Mean Squared Error (MSE): {mse}")
            print(f"Root Mean Squared Error (RMSE): {rmse}")

            # Plot actual vs forecasted values
            plt.figure(figsize=(10,6))
            plt.plot(train_endog.index, train_endog, label='Train Revenue')
            plt.plot(test_endog.index, test_endog, label='Test Revenue')
            plt.plot(test_endog.index, forecast_values, label='Forecasted Revenue', linestyle='--')
            plt.legend()
            plt.title('Train, Test and Forecasted Revenue')
            plt.show()
        return

    # Ensure all data are float64 type to avoid dtype object error
    train_endog = train_endog.astype('float64')
    test_endog = test_endog.astype('float64')
    train_exog = train_exog.astype('float64')
    test_exog = test_exog.astype('float64')

    # Using SARIMAX to model Revenu with exogenous variables on train set
    model = SARIMAX(train_endog, exog=train_exog, order=(1,1,1), seasonal_order=(0,0,0,0))
    model_fit = model.fit(disp=False)
    print(model_fit.summary())

    # Save the model to disk
    with open('../models/sarimax_model.pkl', 'wb') as f:
        pickle.dump(model_fit, f)

    # Forecast on test set with exogenous variables
    if len(test) > 0:
        forecast = model_fit.forecast(steps=len(test), exog=test_exog)

        # Calculate error metrics
        mae = mean_absolute_error(test['Revenu'], forecast)
        mse = mean_squared_error(test['Revenu'], forecast)
        rmse = np.sqrt(mse)

        print(f"Mean Absolute Error (MAE): {mae}")
        print(f"Mean Squared Error (MSE): {mse}")
        print(f"Root Mean Squared Error (RMSE): {rmse}")

        # Plot actual vs forecasted values
        plt.figure(figsize=(10,6))
        plt.plot(train.index, train['Revenu'], label='Train Revenue')
        plt.plot(test.index, test['Revenu'], label='Test Revenue')
        plt.plot(test.index, forecast, label='Forecasted Revenue', linestyle='--')
        plt.legend()
        plt.title('Train, Test and Forecasted Revenue')
        plt.show()

if __name__ == "__main__":
    df = load_data()
    df = prepare_data(df)
    print("Dataframe info after prepare_data:")
    print(df.info())
    print("Non-null counts for 'Revenu':")
    print(df['Revenu'].notnull().sum())
    build_model(df)
