from constant import constants 
def validate_amount(amount:float) -> bool:
        '''Validates if the amount is a positive number and also a valid float 
        args:
        amount: amount to be validated      
        returns: True if valid else False
        '''
        try:
            amount = float(amount)
            if amount <= 0:
                return False
            return True
        except ValueError:
            return False        

def validate_date(date:str) -> bool:
        '''Validates if the date is valid and is in YYYY-MM-DD format 
        args:
        date: date to be validated      
        returns: True if valid else False'''
        try:
            year, month, day = map(int, date.split('-'))
            if year < 0:
                raise ValueError("Invalid year. Year must be a positive integer.")
            if not (1 <= month <= 12):
                raise ValueError("Invalid month. Month must be an integer between 1 and 12.")
            if not (1 <= day <= 31):
                raise ValueError("Invalid day. Day must be an integer between 1 and 31.")
            if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if not (1 <= day <= 29):
                        raise ValueError("Invalid day. Day must be an integer between 1 and 29.")
                else: 
                    if not (1 <= day <= 28):
                        raise ValueError("Invalid day. Day must be an integer between 1 and 28.")
            elif month in [4, 6, 9, 11]:
                if not (1 <= day <= 30):       
                    raise ValueError("Invalid day. Day must be an integer between 1 and 30.")
            return True
        except ValueError:
            return False

def validate_category(category:str) -> bool:
        '''Validates if the category is one of the predefined categories 
        args:
        category: category to be validated      
        returns: True if valid else False'''
        return category.lower() in constants['valid_categories']


def validate_payment_method(payment_method:str) -> bool:
        '''Validates if the payment method is one of the predefined methods 
        args
        payment_method: payment method to be validated     
        returns: True if valid else False'''
        return payment_method.lower() in constants['valid_payment_methods']

def validate_input_year_month_amount(year:int, month:int, amount_limit:float) -> tuple:
    ''' Validates the input year, month, and amount_limit for setting a monthly budget.

    args:
        year (int): The year to validate.
        month (int): The month to validate (1-12).
        amount_limit (float): The budget limit to validate (must be positive).
    returns:
        tuple: A tuple containing a boolean indicating validity and a message.'''
    error_messages = []
    if not (isinstance(year, int) and year > 0):
        error_messages.append("Invalid year. Year must be a positive integer.")
    if not (isinstance(month, int) and 1 <= month <= 12):
        error_messages.append("Invalid month. Month must be an integer between 1 and 12.")
    if not (isinstance(amount_limit, (int, float)) and amount_limit > 0):
        error_messages.append("Invalid amount limit. Amount limit must be a positive number.")
    if error_messages:
        return (False, " ".join(error_messages))
    return (True, "Valid input.")

def validate_year_month(year:int, month:int) -> tuple:
    ''' Validates the input year and month for retrieving a monthly budget.

    args:
        year (int): The year to validate.
        month (int): The month to validate (1-12).
    returns:
        tuple: A tuple containing a boolean indicating validity and a message.'''
    error_messages = []
    if not (isinstance(year, int) and year > 0):
        error_messages.append("Invalid year. Year must be a positive integer.")
    if not (isinstance(month, int) and 1 <= month <= 12):
        error_messages.append("Invalid month. Month must be an integer between 1 and 12.")
    if error_messages:
        return (False, " ".join(error_messages))
    return (True, "Valid input.")

def valid_year_month_in_database(year: int, month: int,database: str, table_name: str) -> bool:
    ''' Checks if the given year and month exists in the given database.
    expense database consists of single table: expenses.
    budget database consists of three tables: monthly_budget, monthly_category_budget, and monthly_payment_method_budget.
    if the year exists in the database, returns True else returns False.

    args:
        year (int): The year to check.
        month (int): The month to check (1-12).
        table_name (str): The name of the table to check.
    returns:
        bool: True if the year and month data exists in the database, else False.'''
    from database_connections import open_database_connection, close_database_connection
    with open_database_connection(database) as object:
        if database == "budget.db":
            cursor = object.cursor()
            cursor.execute(f"SELECT year FROM {table_name} WHERE year = ? AND month = ?", (year, month))
            if cursor.fetchone():
                return True
        elif database == "expense.db":
            cursor = object.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?", (str(year), f"{month:02d}"))
            if cursor.fetchone():
                return True
    return False

def valid_year_in_database(year: int, database: str, table_name: str) -> tuple:
    ''' Checks if the given year exists in the given database.
    expense database consists of single table: expenses.
    budget database consists of three tables: monthly_budget, monthly_category_budget, and monthly_payment_method_budget.
    if the year exists in the database, returns True else returns False.

    args:
        year (int): The year to check.
        database (str): The name of the database file.
        table_name (str): The name of the table to check.
    returns:
        bool: True if the year data exists in the database, else False.'''
    from database_connections import open_database_connection, close_database_connection
    with open_database_connection(database) as object:
        cursor = object.cursor()
        if database == "budget.db":
            cursor.execute(f"SELECT year FROM {table_name} WHERE year = ?", (year,))
            if cursor.fetchone():
                return True
        elif database == "expense.db":
            cursor.execute(f"SELECT * FROM {table_name} WHERE strftime('%Y', date) = ?", (str(year),))
            if cursor.fetchone():
                return True
    return False   
        