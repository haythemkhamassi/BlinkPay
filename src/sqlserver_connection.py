import pyodbc

def connect_to_sql_server():
    """
    Connect to the SQL Server database using Windows Authentication.
    Server: DESKTOP-D9RLU4B
    Database: DWH
    """
    try:
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=HAYTHEM;"
            "DATABASE=DWH;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(connection_string)
        print("Connection successful")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)
        return None

def test_query(conn):
    """
    Run a test query to verify the connection.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        if row:
            print("SQL Server version:", row[0])
        cursor.close()
    except pyodbc.Error as e:
        print("Error executing query:", e)

def fetch_dim_customer_data(conn, limit=None):
    """
    Fetch rows from Dim_Customer table. If limit is None, fetch all rows.
    """
    try:
        cursor = conn.cursor()
        if limit is None:
            query = """
            SELECT [ID_Customer]
                  ,[Gender]
                  ,[Age]
                  ,[Annual_Income]
                  ,[Spending_Score__1_100]
                  ,[Profession]
                  ,[Work_Experience]
                  ,[Family_Size]
              FROM [DWH].[dbo].[Dim_Customer]
            """
        else:
            query = f"""
            SELECT TOP {limit} [ID_Customer]
                  ,[Gender]
                  ,[Age]
                  ,[Annual_Income]
                  ,[Spending_Score__1_100]
                  ,[Profession]
                  ,[Work_Experience]
                  ,[Family_Size]
              FROM [DWH].[dbo].[Dim_Customer]
            """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except pyodbc.Error as e:
        print("Error fetching Dim_Customer data:", e)
        return []

def fetch_distinct_professions(conn):
    """
    Fetch distinct professions from Dim_Customer table.
    """
    try:
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT [Profession]
        FROM [DWH].[dbo].[Dim_Customer]
        ORDER BY [Profession]
        """
        cursor.execute(query)
        professions = [row[0] for row in cursor.fetchall()]
        cursor.close()
        # Convert professions to strings explicitly
        professions_str = [str(prof) for prof in professions]
        return professions_str
    except pyodbc.Error as e:
        print("Error fetching distinct professions:", e)
        return []

if __name__ == "__main__":
    conn = connect_to_sql_server()
    if conn:
        test_query(conn)
        # Example usage of fetch_dim_customer_data
        data = fetch_dim_customer_data(conn)
        print(f"Fetched {len(data)} rows from Dim_Customer")
        conn.close()
