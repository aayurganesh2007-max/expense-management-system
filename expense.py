import sqlite3 as sql
object = sql.connect("expense.db")
cursor = object.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS expenses(expense_id INTEGER PRIMARY KEY AUTOINCREMENT,date DATE, amount REAL ,category VARCHAR, description VARCHAR ,payment_method VARCHAR)")
constants = {'valid_categories': ['food', 'transport', 'utilities', 'entertainment', 'miscellaneous'],
    'valid_payment_methods': ['cash','upi','credit card', 'debit card', 'netbanking','wallet']
}
def validate_amount(amount):
        '''Validates if the amount is a positive number and also a valid float and returns True if valid else returns False'''
        try:
            amount = float(amount)
            if amount <= 0:
                return False
            return True
        except ValueError:
            return False        

def validate_date(date):
        '''Validates if the date is valid and is in YYYY-MM-DD format and returns True if valid else returns False'''
        try:
            year, month, day = map(int, date.split('-'))
            assert 1 <= month <= 12
            assert 1 <= day <= 31
            return True
        except (ValueError, AssertionError):
            return False        

def validate_category(category):
        '''Validates if the category is one of the predefined categories and returns True if valid else returns False'''
        return category.lower() in valid_categories


def validate_payment_method(payment_method):
        '''Validates if the payment method is one of the predefined methods and returns True if valid else returns False'''
        return payment_method.lower() in valid_methods

def add_expense(date, amount, category, description, payment_method):
    '''Adds a new expense record to the expenses table, only if the input data is valid
    returns success message if added successfully else returns error message by specifying all the invalid fields'''
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
        valid_categories = ['food', 'transport', 'utilities', 'entertainment', 'miscellaneous']
        error_message.append(f"Category must be one of the following: {', '.join(valid_categories)}.")
    if not description:
        error_message.append("Description cannot be empty.")
    if not payment_method:
        error_message.append("Payment method cannot be empty.")
    if not validate_payment_method(payment_method):  
        valid_methods = ['cash','upi','credit card', 'debit card', 'netbanking','wallet']
        error_message.append(f"Payment method must be one of the following: {', '.join(valid_methods)}.")
    if error_message:
        return "Error: " + "; ".join(error_message)
    cursor.execute("INSERT INTO expenses (date, amount, category, description, payment_method) VALUES (?,?,?,?,?)", (date, amount, category, description,payment_method))
    object.commit()
    return "Expense added successfully."

def delete_expense(expense_id):
    '''Deletes an expense record from the expenses table based on the provided expense ID.
    returns success message if deleted successfully else returns error message if the ID does not exist'''
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()
    if record:
        cursor.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
        object.commit()
        return "Expense deleted successfully."
    else:
        return "Error: Expense ID does not exist."

def update_expense(expense_id, date=None, amount=None, category=None, description=None, payment_method=None):
    '''Updates an existing expense record in the expenses table based on the provided expense ID and new data(atleast one dat must be updated).Also checks if the input data is valid and only then updates the record.
    returns success message if updated successfully else returns error message if the ID does not exist'''
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()              
    if not record:
        return "Error: Expense ID does not exist."
    fields_to_update = {}
    if date:
        if not validate_date(date):
            return "Error: Date must be in YYYY-MM-DD format."
        fields_to_update['date'] = date             
    if amount:
         if not validate_amount(amount):
            return "Error: Amount must be a valid number."
         fields_to_update['amount'] = amount
    if category:
        if not validate_category(category):
            valid_categories = ['food', 'transport', 'utilities', 'entertainment', 'miscellaneous']
            return f"Error: Category must be one of the following: {', '.join(valid_categories)}."
        fields_to_update['category'] = category
    if description:
        fields_to_update['description'] = description
    if payment_method:
        if not validate_payment_method(payment_method):
            valid_methods = ['cash','upi','credit card', 'debit card', 'netbanking','wallet']
            return f"Error: Payment method must be one of the following: {', '.join(valid_methods)}."
        fields_to_update['payment_method'] = payment_method
    if not fields_to_update:
        return "Error: No fields to update."
    for field, value in fields_to_update.items():
        cursor.execute(f"UPDATE expenses SET {field}=? WHERE expense_id=?", (value, expense_id))    
    object.commit()
    return "Expense updated successfully."

def view_expenses():
    '''Fetches and returns all expense records from the expenses table'''
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    return records

def get_expense_by_id(expense_id):
    '''Fetches and returns a specific expense record based on the provided expense ID only if the id exists'''
    cursor.execute("SELECT * FROM expenses WHERE expense_id=?", (expense_id,))
    record = cursor.fetchone()
    if not record:
        return "Error: Expense ID does not exist."
    return record

def search_expenses(date_range=None, category=None, payment_method=None, amount_range=None):
    '''Fetches and returns expense records based on search criteria like date range, category, payment method, amount range'''
    # This function can be implemented as per specific search criteria requirements
    if date_range:
        cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (date_range[0], date_range[1]))
    elif category:
        cursor.execute("SELECT * FROM expenses WHERE category=?", (category,))
    elif payment_method:
        cursor.execute("SELECT * FROM expenses WHERE payment_method=?", (payment_method,))          
    elif amount_range:
        cursor.execute("SELECT * FROM expenses WHERE amount BETWEEN ? AND ?", (amount_range[0], amount_range[1]))
    records = cursor.fetchall()
    return records

object.commit()

def close_connection():
    '''Closes the database connection'''
    object.close()










    





