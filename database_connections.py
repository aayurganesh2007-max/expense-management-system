import sqlite3 as sql
def open_database_connection(db_name:str)-> "sql.Connection" :
    '''Opens a connection to the specified SQLite database and returns the connection object.
    args:
        db_name (str): The name of the database file to connect to.
    returns:
        sql.Connection: The SQLite database connection object.
    '''
    import sqlite3 as sql
    conn = sql.connect(db_name)
    return conn

def close_database_connection(conn:"sql.Connection")->None:
    '''Closes the given SQLite database connection.
    args:
        conn (sql.Connection): The SQLite database connection object to close.
    returns:
        None
    '''
    conn.close()