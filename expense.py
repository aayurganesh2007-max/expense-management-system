from database_connections import open_database_connection, close_database_connection
import sqlite3 as sql
object = open_database_connection("expense.db")
cursor= object.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS expenses(expense_id INTEGER PRIMARY KEY AUTOINCREMENT,date DATE, amount REAL ,category VARCHAR, description VARCHAR ,payment_method VARCHAR)")
# usage of constants helps reduce redundancy and makes it easier to update valid categories and payment methods in one place which is imported from constant.py
from constant import constants
# Importing validation functions from validators.py to validate input data before database operations
from validators import validate_amount, validate_date, validate_category, validate_payment_method

def notify_budget_exceeding_expense(date:str, amount:float, category:str, payment_method:str) -> tuple:
    '''Checks if adding a new expense would exceed the set monthly budget for the given date, category, and payment method.
    args:
    date: date of the expense in YYYY-MM-DD format      
    amount: amount of the expense as a positive number
    category: category of the expense from predefined categories
    payment_method: payment method of the expense from predefined methods
    returns: a tuple of boolean value and message'''
    year, month, _ = map(int, date.split('-'))
    error_messages = []
    from budget import balance_budget
    valid,balance_amount= balance_budget(year,month,category)
    excess1 = amount - balance_amount
    if valid and excess1> 0:
            error_messages.append(f"Adding this expense exceeds the budget for category '{category}'.By amount'{excess1}'")    
    valid2,balance_amount2= balance_budget(year,month,payment_method=payment_method)
    excess2 = amount - balance_amount2
    if valid2 and excess2> 0:
            error_messages.append(f"Adding this expense exceeds the budget for payment method '{payment_method}'.By amount'{excess2}'")
    valid3,balance_amount3= balance_budget(year,month)
    excess3 = amount - balance_amount3
    if valid3 and excess3> 0:
            error_messages.append(f"Adding this expense exceeds the overall monthly budget.By amount'{excess3}'")
    if error_messages:  
        return (False," ; ".join(map(str,error_messages)))
    return (True,"Within budget limits.")
    
    

def add_expense(date:str, amount:float, category:str, description:str, payment_method:str,approval:bool = False)-> tuple:
    '''Adds a new expense record to the expenses table, only if the input data is valid
    and also checks if adding the expense would exceed the set monthly budget.or category/payment method specific budget.
    returns success message if added successfully else returns error message by specifying all the invalid fields and budget exceeding message if any
    args:
    date: date of the expense in YYYY-MM-DD format      
    amount: amount of the expense as a positive number
    category: category of the expense from predefined categories
    description: description of the expense as a string
    payment_method: payment method of the expense from predefined methods
    approval: boolean flag to indicate if user has approved adding expense that exceeds budget
    returns: a tuple of boolean value and success or error message'''
    error_message =[]
    if not validate_amount(amount):
        error_message.append("Amount must be a valid number.")
    if not date:
        error_message.append("Date cannot be empty.")
    if not validate_date(date):
        error_message.append("Date must be in YYYY-MM-DD format.")
    if not category:
        error_message.append("Category cannot be empty.")
    if not validate_category(category):
        error_message.append(f"Category must be one of the following: {', '.join(constants['valid_categories'])}.")
    if not description:
        error_message.append("Description cannot be empty.")
    if not payment_method:
        error_message.append("Payment method cannot be empty.")
    if not validate_payment_method(payment_method):  
        error_message.append(f"Payment method must be one of the following: {', '.join(constants['valid_payment_methods'])}.")
    if error_message:
        # returns both boolean value and error message and to make it more expandable for future if needed
        return (False,"Error: " + "; ".join(error_message))
    if not approval:
        valid,message= notify_budget_exceeding_expense(date, amount, category, payment_method)
        if not valid:
            return (False,message)
        cursor.execute("INSERT INTO expenses (date, amount, category, description, payment_method) VALUES (?,?,?,?,?)", (date, amount, category, description,payment_method))
        object.commit()
    cursor.execute("INSERT INTO expenses (date, amount, category, description, payment_method) VALUES (?,?,?,?,?)", (date, amount, category, description,payment_method))
    object.commit()
    return (True,"Expense added successfully.")

def delete_expense(expense_id:int) -> tuple:
    '''Deletes an expense record from the expenses table based on the provided expense ID.
    returns success message if deleted successfully else returns error message if the ID does not exist
    args:  
    expense_id: ID of the expense to be deleted
    returns: a tuple of boolean value and success or error message'''
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()
    if record:
        cursor.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
        object.commit()
        return (True,"Expense deleted successfully.")
    else:
        return (False,"Error: Expense ID does not exist.")

def update_expense(expense_id:int, date:str=None, amount:float=None, category:str=None, description:str=None, payment_method:str=None,approval:bool = False) -> tuple:
    '''Updates an existing expense record in the expenses table based on the provided expense ID and new data(atleast one dat must be updated).Also checks if the input data is valid and only then updates the record.
    returns success message if updated successfully else returns error message if the ID does not exist
    args:
    expense_id: ID of the expense to be updated
    date: new date of the expense in YYYY-MM-DD format
    amount: new amount of the expense as a positive number
    category: new category of the expense from predefined categories
    description: new description of the expense as a string
    payment_method: new payment method of the expense from predefined methods
    approval: boolean flag to indicate if user has approved adding expense that exceeds budget
    returns: a tuple of boolean value and success or error message'''
    error_message2 =[]
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()              
    if not record:
        error_message2.append("Error: Expense ID does not exist.")
    fields_to_update = {}
    
    if date:
        if not validate_date(date):
            error_message2.append("Error: Date must be in YYYY-MM-DD format.")
        fields_to_update['date'] = date             
    if amount:
         if not validate_amount(amount):
            error_message2.append("Error: Amount must be a valid number.")
         fields_to_update['amount'] = amount
    if category:
        if not validate_category(category):
            error_message2.append(f"Error: Category must be one of the following: {', '.join(constants['valid_categories'])}.")
        fields_to_update['category'] = category
    if description:
        fields_to_update['description'] = description
    if payment_method:
        if not validate_payment_method(payment_method):
            error_message2.append(f"Error: Payment method must be one of the following: {', '.join(constants['valid_payment_methods'])}.")
        fields_to_update['payment_method'] = payment_method
    if not fields_to_update:
        error_message2.append("Error: At least one field must be provided for update.")
    if error_message2:
        return (False," ; ".join(error_message2))
    for field, value in fields_to_update.items():
        if not approval:
            valid,message= notify_budget_exceeding_expense(date if field=='date' else record[1], amount if field=='amount' else record[2], category if field=='category' else record[3], payment_method if field=='payment_method' else record[5])
            if not valid:
                return (False,message)
            cursor.execute(f"UPDATE expenses SET {field}=? WHERE expense_id=?", (value, expense_id))
            object.commit()
        cursor.execute(f"UPDATE expenses SET {field}=? WHERE expense_id=?", (value, expense_id))    
        object.commit()
    return (True,"Expense updated successfully.")

def view_expenses()-> tuple:
    '''Fetches and returns all expense records from the expenses table
    args: None
    returns: a tuple of boolean value and list of expense records'''
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    return (True,records)

def get_expense_by_id(expense_id:int) -> tuple:
    '''Fetches and returns a specific expense record based on the provided expense ID only if the id exists
    args:  
    expense_id: ID of the expense to be fetched
    returns: a tuple of boolean value and expense record or error message'''
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()
    if not record:
        return (False,"Error: Expense ID does not exist.")
    return (True,record)

def search_expenses(date_range:tuple=None, category:str=None, payment_method:str=None, amount_range:tuple=None) -> tuple:
    '''Fetches and returns expense records based on search criteria like date range, category, payment method, amount range
    args:
    date_range: tuple of start date and end date in YYYY-MM-DD format
    category: category of the expense from predefined categories
    payment_method: payment method of the expense from predefined methods
    amount_range: tuple of minimum amount and maximum amount
    returns: a tuple of boolean value and list of expense records or error message'''
    if date_range:
        if (validate_date(date_range[0]) is False) or (validate_date(date_range[1]) is False):
            return (False,"Error: Date must be in YYYY-MM-DD format.")
        cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (date_range[0], date_range[1]))
    elif category:
        if not validate_category(category):
            return (False,f"Error: Category must be one of the following: {', '.join(constants['valid_categories'])}.")
        cursor.execute("SELECT * FROM expenses WHERE category=?", (category,))
    elif payment_method:
        if not validate_payment_method(payment_method):
            return (False,f"Error: Payment method must be one of the following: {', '.join(constants['valid_payment_methods'])}.")
        cursor.execute("SELECT * FROM expenses WHERE payment_method=?", (payment_method,))          
    elif amount_range:
        if (not validate_amount(amount_range[0])) or (not validate_amount(amount_range[1])):
            return (False,"Error: Amount must be a valid number.")
        cursor.execute("SELECT * FROM expenses WHERE amount BETWEEN ? AND ?", (amount_range[0], amount_range[1]))
    records = cursor.fetchall()
    return (True,records)


object.commit()
close_database_connection(object)