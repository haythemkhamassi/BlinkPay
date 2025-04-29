import pyodbc

def connect_to_dwh():
    server = 'HAYTHEM'
    database = 'DWH'
    # Use Trusted_Connection for Microsoft Authentication (Windows Authentication)
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        conn = pyodbc.connect(connection_string)
        print("Connection to the DWH database was successful.")
        return conn
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

if __name__ == "__main__":
    connect_to_dwh()
