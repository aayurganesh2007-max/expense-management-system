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

def run_db_operation(operation):
    ''' Safely executes a database operation.

    The wrapped operation MUST return:
        (bool, data_or_message)

    If any unexpected database or runtime error occurs,
    this function guarantees returning:
        (False, error_message)

    args:
        operation (callable): A function performing a DB operation.
    returns:
        tuple: If successful, returns the operation result as a tuple.
               If unsuccessful, returns a tuple containing a boolean indicating failure and the error message.
    '''
    try:
        return operation()
    except Exception as e:
        return (False, str(e))