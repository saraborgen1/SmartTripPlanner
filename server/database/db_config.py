import pyodbc

def get_connection():
    server = 'SmartTripDB.mssql.somee.com'
    database = 'SmartTripDB'
    username = 'tripuser1'
    password = 'Trip@1234!'

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    return pyodbc.connect(conn_str)


