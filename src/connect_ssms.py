import pyodbc

import pandas as pd

def connect_to_ssms():
    server = 'HAYTHEM'
    database = 'DWH'
    # Use Windows Authentication
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'
    )
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection to the database was successful!")
        return conn
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

def fetch_dim_product_data(conn):
    query = "SELECT * FROM Dim_Product"
    try:
        df = pd.read_sql(query, conn)
        print(f"Fetched {len(df)} rows from Dim_Product table.")
        return df
    except Exception as e:
        print(f"Failed to fetch data from Dim_Product: {e}")
        return None

def get_dim_product_columns(conn):
    query = "SELECT TOP 1 * FROM Dim_Product"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        print("Columns in Dim_Product table:")
        for col in columns:
            print(col)
        return columns
    except Exception as e:
        print(f"Failed to get columns from Dim_Product: {e}")
        return None

if __name__ == "__main__":
    conn = connect_to_ssms()
    if conn:
        columns = get_dim_product_columns(conn)
        df = fetch_dim_product_data(conn)
        # You can now use df for your machine learning model
        conn.close()
