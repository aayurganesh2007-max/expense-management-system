from database_connections import open_database_connection, close_database_connection
import sqlite3 as sql
object = open_database_connection("budget.db")
cursor = object.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS monthly_budget(id INTEGER PRIMARY KEY AUTOINCREMENT,year int,month int, amount_limit REAL, CONSTRAINT  year_month UNIQUE(year,month))")
cursor.execute("CREATE TABLE IF NOT EXISTS monthly_category_budget(id INTEGER PRIMARY KEY AUTOINCREMENT,year int,month int, category VARCHAR, amount_limit REAL ,CONSTRAINT year_month_category UNIQUE(year,month,category))")
cursor.execute("CREATE TABLE IF NOT EXISTS monthly_payment_method_budget(id INTEGER PRIMARY KEY AUTOINCREMENT,year int,month int, payment_method VARCHAR, amount_limit REAL , CONSTRAINT  year_month_payment UNIQUE(year,month,payment_method))")
# Importing validation functions from validators.py to validate input data before database operations
from validators import validate_input_year_month_amount, validate_year_month

def set_update_monthly_budget(year:int, month:int, amount_limit:float) -> tuple:
    ''' Checks if a given year and month combination exists in the table
    if yes it updates the existing data with the new amount
    otherwise creates a new row with the valid budget.

     args:
        year (int): The year for which the budget is to be set.
        month (int): The month for which the budget is to be set (1-12).
        amount_limit (float): The budget limit for the specified month and year.
     returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.'''
    valid,message = validate_input_year_month_amount(year, month, amount_limit)
    if not valid:
        return (False, message)
    cursor.execute("SELECT * FROM monthly_budget WHERE year = ? AND month = ?", (year, month))
    existing_budget = cursor.fetchone()
    if existing_budget:
        cursor.execute("UPDATE monthly_budget SET amount_limit = ? WHERE year = ? AND month = ?", (amount_limit, year, month))
        object.commit()
        return (True, "Monthly budget updated successfully.")
    cursor.execute("INSERT INTO monthly_budget (year, month, amount_limit) VALUES (?, ?, ?)", (year, month, amount_limit))
    object.commit()
    return (True, "Monthly budget set successfully.")

def set_update_monthly_category_budget(year:int, month:int, category:str, amount_limit:float) -> tuple:
    ''' Checks if a given year, month and category combination exists in the table
    if yes it updates the existing data with the new amount
    otherwise creates a new row with the valid budget.

     args:
        year (int): The year for which the budget is to be set.
        month (int): The month for which the budget is to be set (1-12).
        category (str): The category for which the budget is to be set.
        amount_limit (float): The budget limit for the specified month, year and category.
     returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.'''
    from expense import validate_category   
    valid,message = validate_input_year_month_amount(year, month, amount_limit)
    if not valid:
        if not validate_category(category):
            return (False,message+"Invalid category. Please provide a valid category.")
        return (False, message)
    cursor.execute("SELECT * FROM monthly_category_budget WHERE year = ? AND month = ? AND category = ?", (year, month, category))
    existing_budget = cursor.fetchone()
    if existing_budget:
        cursor.execute("UPDATE monthly_category_budget SET amount_limit = ? WHERE year = ? AND month = ? AND category = ?", (amount_limit, year, month, category))
        object.commit()
        return (True, "Monthly category budget updated successfully.")
    cursor.execute("INSERT INTO monthly_category_budget (year, month, category, amount_limit) VALUES (?, ?, ?, ?)", (year, month, category, amount_limit))
    object.commit()
    return (True, "Monthly category budget set successfully.")

def set_update_monthly_payment_method_budget(year:int, month:int, payment_method:str, amount_limit:float) -> tuple:
    ''' Checks if a given year, month and payment_method combination exists in the table
    if yes it updates the existing data with the new amount
    otherwise creates a new row with the valid budget.

     args:
        year (int): The year for which the budget is to be set.
        month (int): The month for which the budget is to be set (1-12).
        payment_method (str): The payment method for which the budget is to be set.
        amount_limit (float): The budget limit for the specified month, year and payment method.
     returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.'''
    from expense import validate_payment_method   
    valid,message = validate_input_year_month_amount(year, month, amount_limit)
    if not valid:
        if not validate_payment_method(payment_method):
            return (False,message+"Invalid payment method. Please provide a valid payment method.")
        return (False, message)
    cursor.execute("SELECT * FROM monthly_payment_method_budget WHERE year = ? AND month = ? AND payment_method = ?", (year, month, payment_method))
    existing_budget = cursor.fetchone()
    if existing_budget:
        cursor.execute("UPDATE monthly_payment_method_budget SET amount_limit = ? WHERE year = ? AND month = ? AND payment_method = ?", (amount_limit, year, month, payment_method))
        object.commit()
        return (True, "Monthly payment method budget updated successfully.")
    cursor.execute("INSERT INTO monthly_payment_method_budget (year, month, payment_method, amount_limit) VALUES (?, ?, ?, ?)", (year, month, payment_method, amount_limit))
    object.commit()
    return (True, "Monthly payment method budget set successfully.")

def get_monthly_budget(year:int, month:int,category:str=None,payment_method:str=None) -> tuple:
    ''' Retrieves the budget limit for a specific month and year.
        and if category is provided it returns budget limit for that category 
        and if payment method is provided it returns budget limit for that payment method
        args:
            year (int): The year for which the budget is to be retrieved.
            month (int): The month for which the budget is to be retrieved (1-12).
        returns:
            tuple: A tuple containing a boolean indicating success or failure, and the budget limit or an error message.'''
    if category:
        from expense import validate_category   
        if not validate_category(category):
            return (False, "Invalid category. Please provide a valid category.")
        cursor.execute("SELECT amount_limit FROM monthly_category_budget WHERE year = ? AND month = ? AND category = ?", (year, month, category))
        budget = cursor.fetchone()
        if budget:
            return (True, budget[0])
    if payment_method:
        from expense import validate_payment_method
        if not validate_payment_method(payment_method):
            return (False, "Invalid payment method. Please provide a valid payment method.")
        cursor.execute("SELECT amount_limit FROM monthly_payment_method_budget WHERE year = ? AND month = ? AND payment_method = ?", (year, month, payment_method))
        budget = cursor.fetchone()
        if budget:
            return (True, budget[0])
    valid,message = validate_year_month(year, month)
    if not valid:
        return (False, message)
    cursor.execute("SELECT amount_limit FROM monthly_budget WHERE year = ? AND month = ?", (year, month))
    budget = cursor.fetchone()
    if budget:
        return (True, budget[0])
    return (False, "No budget set for the specified parameters.")
    
def monthly_expense(year:int, month:int,category:str = None,payment_method:str = None) -> float:
    '''Calculates the total expenses for a given month and year.
        if category is provided it returns total expenses for that category 
        and if payment method is provided it returns total expenses for that payment method

    args:
        year (int): The year for which to calculate total expenses.
        month (int): The month for which to calculate total expenses (1-12).        
        category (str): The category for which to calculate total expenses (optional).
        payment_method (str): The payment method for which to calculate total expenses (optional).

    returns:
        tuple: A tuple containing a boolean indicating success or failure, and the total expenses or an error message.'''
    from database_connections import open_database_connection, close_database_connection
    object = open_database_connection("expense.db")
    cursor = object.cursor()
    if category:
        from expense import validate_category
        if not validate_category(category):
            return (False, "Invalid category. Please provide a valid category.")
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? AND category = ?", (str(year), f"{month:02d}", category))
        total_expense = cursor.fetchone()[0]
        close_database_connection(object)
        return (True,total_expense if total_expense else 0.0)
    if payment_method:
        from expense import validate_payment_method
        if not validate_payment_method(payment_method):
            return (False, "Invalid payment method. Please provide a valid payment method.")
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? AND payment_method = ?", (str(year), f"{month:02d}", payment_method))
        total_expense = cursor.fetchone()[0]
        close_database_connection(object)
        return (True,total_expense if total_expense else 0.0)
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?", (str(year), f"{month:02d}"))
    total_expense = cursor.fetchone()[0]
    close_database_connection(object)
    return (True,total_expense if total_expense else 0.0)

def balance_budget(year:int, month:int, category:str=None, payment_method:str=None) -> tuple:
    '''Calculates the remaining budget for a given month and year.
       if category is provided it returns remaining budget for that category 
       and if payment method is provided it returns remaining budget for that payment method
       and if budget is exceeded it returns by how much it is exceeded.

    args:
        year (int): The year for which to calculate the remaining budget.
        month (int): The month for which to calculate the remaining budget (1-12).
    returns:
        tuple: A tuple containing a boolean indicating success or failure, and the remaining budget or an error message.'''
    valid1,total_budget = get_monthly_budget(year, month, category, payment_method)
    if not valid1:
        return (False, total_budget)
    valid2,total_expense = monthly_expense(year, month, category, payment_method)
    if not valid2:
        return (False, total_expense)
    remaining_budget = total_budget - total_expense
    if remaining_budget < 0:
        return (False, "Budget exceeded by {:.2f}".format(-remaining_budget))
    return (True, remaining_budget)

def get_all_budgets() -> list:
    '''Retrieves all monthly budgets from the database.

    returns:
        list: A list of tuples, each containing the year, month, and amount_limit of a budget.'''
    cursor.execute("SELECT year, month, amount_limit FROM monthly_budget")
    budgets = cursor.fetchall()
    return budgets

def get_all_category_budgets(year:int=None, month:int=None) -> list:
    '''Retrieves all monthly category budgets for a specific month and year from the database.
    if only year is provided, retrieves all category budgets for that year.
    if year and month are not provided, retrieves all category budgets.

    args:
        year (int): The year for which to retrieve category budgets.(optional)
        month (int): The month for which to retrieve category budgets (1-12).(optional)
    returns:
        list: A tuple of a boolean and a list of tuples, each containing the category and amount_limit of a budget.or an error message.'''
    
    if year and month:
        valid,message = validate_year_month(year, month)
        if not valid:
            return(False,message)
        cursor.execute("SELECT category, amount_limit FROM monthly_category_budget WHERE year = ? AND month = ?", (year, month))
        budgets = cursor.fetchall()
        return (True,budgets)
    if year:
        cursor.execute("SELECT category, amount_limit FROM monthly_category_budget WHERE year = ?", (year,))
        budgets = cursor.fetchall()
        return (True,budgets)
    cursor.execute("SELECT category, amount_limit FROM monthly_category_budget")
    budgets = cursor.fetchall()
    return (True,budgets)

def get_all_payment_method_budgets(year:int=None, month:int=None) -> list:
    '''Retrieves all monthly payment method budgets for a specific month and year from the database.
    if only year is provided, retrieves all payment method budgets for that year.
    if year and month are not provided, retrieves all payment method budgets.

    args:
        year (int): The year for which to retrieve payment method budgets.(optional)
        month (int): The month for which to retrieve payment method budgets (1-12).(optional)
    returns:
        list: A tuple of a boolean and a list of tuples, each containing the payment method and amount_limit of a budget.or an error message.'''
    if year and month:
        valid,message = validate_year_month(year, month)
        if not valid:
            return(False,message)
        cursor.execute("SELECT payment_method, amount_limit FROM monthly_payment_method_budget WHERE year = ? AND month = ?", (year, month))
        budgets = cursor.fetchall()
        return (True,budgets)   
    if year:
        cursor.execute("SELECT payment_method, amount_limit FROM monthly_payment_method_budget WHERE year = ?", (year,))
        budgets = cursor.fetchall()
        return (True,budgets)
    cursor.execute("SELECT payment_method, amount_limit FROM monthly_payment_method_budget")
    budgets = cursor.fetchall()
    return (True,budgets)

def delete_budget_limit(year:int, month:int, category:str=None, payment_method:str=None) -> tuple:
    '''Deletes the budget limit for a specific month and year.
        if category is provided it deletes budget limit for that category 
        and if payment method is provided it deletes budget limit for that payment method

    args:
        year (int): The year for which the budget is to be deleted.
        month (int): The month for which the budget is to be deleted (1-12).
    returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.'''
    if category:
        from expense import validate_category
        if not validate_category(category):
            return (False, "Invalid category. Please provide a valid category.")
        cursor.execute("DELETE FROM monthly_category_budget WHERE year = ? AND month = ? AND category = ?", (year, month, category))
        object.commit()
        return (True, "Monthly category budget deleted successfully.")
    if payment_method:
        from expense import validate_payment_method
        if not validate_payment_method(payment_method):
            return (False, "Invalid payment method. Please provide a valid payment method.")
        cursor.execute("DELETE FROM monthly_payment_method_budget WHERE year = ? AND month = ? AND payment_method = ?", (year, month, payment_method))
        object.commit()
        return (True, "Monthly payment method budget deleted successfully.")
    cursor.execute("DELETE FROM monthly_budget WHERE year = ? AND month = ?", (year, month))
    object.commit()
    return (True, "Monthly budget deleted successfully.")
object.commit()

close_database_connection(object)