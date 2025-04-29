import pyodbc

def connect_to_dwh():
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
        with pyodbc.connect(connection_string) as conn:
            print("Connection to DWH database successful.")
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION;")
            row = cursor.fetchone()
            print("SQL Server version:", row[0])
    except Exception as e:
        print("Error connecting to database:", e)

if __name__ == "__main__":
    connect_to_dwh()
