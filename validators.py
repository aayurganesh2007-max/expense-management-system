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
            assert 1 <= month <= 12
            assert 1 <= day <= 31
            if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    assert day <= 29
                else:
                    assert day <= 28 
            elif month in [4, 6, 9, 11]:
                assert day <= 30       
            return True
        except (ValueError, AssertionError):
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