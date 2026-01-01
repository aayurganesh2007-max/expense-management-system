import pandas as pd
from database_connections import open_database_connection, close_database_connection
import csv
def fetch_expense_data(db_name: str) -> pd.DataFrame:
    ''' Generates a pandas DataFrame containing all expenses from the database.
    args:
        db_name (str): The name of the database file.
    returns:
        pd.DataFrame: A DataFrame containing all expense records.'''
    conn = open_database_connection(db_name)
    query = "SELECT * FROM expenses"
    df = pd.read_sql_query(query, conn)
    close_database_connection(conn)
    return df

def fetch_budget_data(db_name: str, table_name: str) -> pd.DataFrame:
    ''' Generates a pandas DataFrame containing all budget data from the database.
    args:
        db_name (str): The name of the database file.
        table_name (str): The name of the budget table.
    returns:
        pd.DataFrame: A DataFrame containing all budget records.'''
    conn = open_database_connection(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    close_database_connection(conn)
    return df

def refresh_expense_df():
    '''Refresh the global expense DataFrame by fetching the latest data from the database.
    And also convert date column to date time to ensure smooth usage
    
    This function updates the global `expense_pd_df` variable with the current state of the
    expense database. It should be called after any insert, update, or delete operations to
    ensure the DataFrame reflects the latest changes.
    Args:
        None
    Returns:
        None'''
    global expense_pd_df
    expense_pd_df = fetch_expense_data('expense.db')
    expense_pd_df['date'] = pd.to_datetime(expense_pd_df['date'])
    #print(expense_pd_df)

def refresh_monthly_budget_dfs():
    '''Refresh the global budget DataFrames by fetching the latest data from the database.
    
    This function updates the global `monthly_budget_pd_df`, variables with the current state of the budget databases.
    It should be called after any insert, update, or delete operations to ensure the DataFrames
    reflect the latest changes.
    Args:
        None
    Returns:
        None'''

    global monthly_budget_pd_df
    monthly_budget_pd_df = fetch_budget_data('budget.db', 'monthly_budget')
    
def refresh_monthly_category_budget_dfs():
    '''Refresh the global budget DataFrames by fetching the latest data from the database.
    
    This function updates the global `monthly_category_budget_pd_df`, variables with the current state of the budget databases.
    It should be called after any insert, update, or delete operations to ensure the DataFrames
    reflect the latest changes.
    Args:
        None
    Returns:
        None'''
    global monthly_category_budget_pd_df
    monthly_category_budget_pd_df = fetch_budget_data('budget.db', 'monthly_category_budget')

def refresh_monthly_payment_method_budget_dfs():
    '''Refresh the global budget DataFrames by fetching the latest data from the database.
    This function updates the global `monthly_payment_method_budget_pd_df`, variables with the current state of the budget databases.
    It should be called after any insert, update, or delete operations to ensure the DataFrames
    reflect the latest changes.
    Args:
        None
    Returns:
        None'''
    global monthly_payment_method_budget_pd_df
    monthly_payment_method_budget_pd_df = fetch_budget_data('budget.db', 'monthly_payment_method_budget')

"""
print(refresh_expense_df())

print(refresh_monthly_budget_dfs())
print(refresh_monthly_category_budget_dfs())
print(refresh_monthly_payment_method_budget_dfs())"""

def get_each_monthly_expense_year_df(year:int) -> tuple:
    ''' Retrieves total expenses for each month in a given year  and also the maximum spending month.
    args:
        year (int): The year for which to retrieve monthly expenses.
    returns:
        tuple: A tuple containing a DataFrame with months and their corresponding total expenses,
               and a dictionary with the maximum spending month and amount.'''
    #to create a var
    refresh_expense_df()
    # select rows for the year and copy to avoid SettingWithCopyWarning
    df_year = expense_pd_df[expense_pd_df['date'].dt.year == year].copy()
    # extract month number
    df_year['month_num'] = (df_year['date']).dt.month
    # aggregate sums by month number
    monthly = df_year.groupby('month_num')['amount'].sum()
    # ensure all 12 months present (1..12) with zeros for missing months
    monthly = monthly.reindex(range(1, 13), fill_value=0)
    # reset index to turn Series into DataFrame
    monthly_expenses = monthly.reset_index()
    # map month numbers to month names
    months = {i+1: name for i, name in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])} 
    monthly_expenses['month'] = monthly_expenses['month_num'].map(months)
    # reorder columns to ['month', 'amount']
    monthly_expenses = monthly_expenses[['month', 'amount']]
    # find maximum spending month
    max_month = monthly_expenses.loc[monthly_expenses['amount'].idxmax()]
    max_spending = {'month': max_month['month'], 'amount': float(max_month['amount'])}
    return (monthly_expenses, max_spending)

def get_daily_expense_month_year_df(year:int, month:int) -> tuple:
    ''' Retrieves total expenses for each day in a given month 
    and also the maximum spending day.
    args:
        year (int): The year for which to retrieve daily expenses.
        month (int): The month for which to retrieve daily expenses.
    returns:
        tuple: A tuple containing a DataFrame with days and their corresponding total expenses,
               and a dictionary with the maximum spending day and amount.'''
    refresh_expense_df()
    # format month to two digits
    month_str = f"{month:02d}"
    # select rows for the specified year and month
    df_month = expense_pd_df.loc[(expense_pd_df['date'].dt.year == year) & (expense_pd_df['date'].dt.month == month)].copy()
    # extract day number
    df_month['day_num'] = (df_month['date']).dt.day
    # aggregate sums by day number
    daily = df_month.groupby('day_num')['amount'].sum()
    # ensure all days of the month present with zeros for missing days
    from calendar import monthrange
    # retrieve number of days in the month(also handles leap years)
    num_days = monthrange(year, month)[1]
    #fill missing days with 0
    daily = daily.reindex(range(1, num_days + 1), fill_value=0)
    # reset index to turn Series into DataFrame
    daily_expenses = daily.reset_index()
    # rename columns to ['day', 'amount']
    daily_expenses.columns = ['day', 'amount']
    # find maximum spending day
    max_day = daily_expenses.loc[daily_expenses['amount'].idxmax()]
    max_spending = {'day': int(max_day['day']), 'amount': float(max_day['amount'])}
    return (daily_expenses, max_spending) 

def get_category_expense_month_year_df(year:int, month:int) -> tuple:
    ''' Retrieves total expenses for each category in a given month  and also the maximum spent category.
    args:
        year (int): The year for which to retrieve category expenses.
        month (int): The month for which to retrieve category expenses.
    returns:
        tuple : A DataFrame with categories and their corresponding total expenses,
                and a dictionary with the maximum spent category and amount.'''
    refresh_expense_df()
    # format month to two digits
    month_str = f"{month:02d}"
    # select rows for the specified year and month
    df_month = expense_pd_df.loc[(expense_pd_df['date'].dt.year == year) & (expense_pd_df['date'].dt.month == month)].copy()
    # aggregate sums by category
    category_expenses = df_month.groupby('category')['amount'].sum().reset_index()
    # rename columns to ['category', 'amount']
    # fill missing categories with 0
    from constant import constants
    valid_categories = constants['valid_categories']
    category_expenses = category_expenses.set_index('category').reindex(valid_categories, fill_value=0).reset_index()
    category_expenses
    category_expenses.columns = ['category', 'amount']
    # find maximum spent category
    max_category = category_expenses.loc[category_expenses['amount'].idxmax()]
    max_spending = {'category': max_category['category'], 'amount': float(max_category['amount'])}
    return (category_expenses, max_spending)

def get_payment_method_expense_month_year_df(year:int, month:int) -> tuple:
    ''' Retrieves total expenses for each payment method in a given month after  and the maximum spent payment method.
    args:
        year (int): The year for which to retrieve payment method expenses.
        month (int): The month for which to retrieve payment method expenses.
    returns:
        tuple: A DataFrame with payment methods and their corresponding total expenses,
                and a dictionary with the maximum spent payment method and amount.'''
    refresh_expense_df()
    # format month to two digits
    month_str = f"{month:02d}"
    # select rows for the specified year and month
    df_month = expense_pd_df.loc[(expense_pd_df['date'].dt.year == year) & (expense_pd_df['date'].dt.month == month)].copy()
    # aggregate sums by payment method
    payment_method_expenses = df_month.groupby('payment_method')['amount'].sum().reset_index()
    # rename columns to ['payment_method', 'amount']
    # fill missing payment methods with 0
    from constant import constants
    valid_payment_methods = constants['valid_payment_methods']
    payment_method_expenses = payment_method_expenses.set_index('payment_method').reindex(valid_payment_methods, fill_value=0).reset_index()
    payment_method_expenses.columns = ['payment_method', 'amount']
    # find maximum spent payment method
    max_payment_method = payment_method_expenses.loc[payment_method_expenses['amount'].idxmax()]
    max_spending = {'payment_method': max_payment_method['payment_method'], 'amount': float(max_payment_method['amount'])}
    return (payment_method_expenses, max_spending)

def get_each_monthly_budget_year_df(year:int) -> tuple:
    ''' retrieves monthly budget limits for each month in a given year and also the maximum budget month.
    args:
        year (int): The year for which to retrieve monthly budgets.
    returns:
        tuple: A DataFrame with months and their corresponding budget limits,
               and a dictionary with the maximum budget month and amount.'''
    refresh_monthly_budget_dfs()
    # select rows for the year
    df_year = monthly_budget_pd_df[monthly_budget_pd_df['year'] == year].copy()
    # ensure all 12 months present (1..12) with zeros for missing months
    monthly = df_year.set_index('month')['amount_limit'].reindex(range(1, 13), fill_value=0)
    # reset index to turn Series into DataFrame
    monthly = monthly.reset_index()
    # map month numbers to month names\
    months = {i+1: name for i, name in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])} 
    monthly['month'] = monthly['month'].map(months)
    # reorder columns to ['month', 'amount_limit']
    monthly.columns = ['month', 'amount_limit']
    # find maximum budget month
    max_month = monthly.loc[monthly['amount_limit'].idxmax()]
    max_budget = {'month': str(max_month['month']), 'amount': float(max_month['amount_limit'])}
    return (monthly, max_budget)

def get_category_monthly_budget_year_df(year:int, month:int) -> tuple:
    ''' retrieves category-wise budget limits for a given month and also the maximum budget category.
    args:
        year (int): The year for which to retrieve category budgets.
        month (int): The month for which to retrieve category budgets.
    returns:
        tuple: A DataFrame with categories and their corresponding budget limits,
               and a dictionary with the maximum budget category and amount.'''
    refresh_monthly_category_budget_dfs()
    # select rows for the specified year and month
    df_month = monthly_category_budget_pd_df[(monthly_category_budget_pd_df['year'] == year) & (monthly_category_budget_pd_df['month'] == month)].copy()
    # fill missing categories with 0
    from constant import constants
    valid_categories = constants['valid_categories']
    category_budgets = df_month.set_index('category')['amount_limit'].reindex(valid_categories, fill_value=0).reset_index()
    # reorder columns to ['category', 'amount_limit']
    category_budgets.columns = ['category', 'amount_limit']
    # find maximum budget category
    max_category = category_budgets.loc[category_budgets['amount_limit'].idxmax()]
    max_budget = {'category': max_category['category'], 'amount': float(max_category['amount_limit'])}
    return (category_budgets, max_budget)

def get_payment_method_monthly_budget_year_df(year:int, month:int) -> tuple:
    ''' retrieves payment method-wise budget limits for a given month and also the maximum budget payment method.
    args:
        year (int): The year for which to retrieve payment method budgets.
        month (int): The month for which to retrieve payment method budgets.
    returns:
        tuple: A DataFrame with payment methods and their corresponding budget limits,
               and a dictionary with the maximum budget payment method and amount.'''
    refresh_monthly_payment_method_budget_dfs()
    # select rows for the specified year and month
    df_month = monthly_payment_method_budget_pd_df[(monthly_payment_method_budget_pd_df['year'] == year) & (monthly_payment_method_budget_pd_df['month'] == month)].copy()
    # fill missing payment methods with 0
    from constant import constants
    valid_payment_methods = constants['valid_payment_methods']
    payment_method_budgets = df_month.set_index('payment_method')['amount_limit'].reindex(valid_payment_methods, fill_value=0).reset_index()
    # reorder columns to ['payment_method', 'amount_limit']
    payment_method_budgets.columns = ['payment_method', 'amount_limit']
    # find maximum budget payment method
    max_payment_method = payment_method_budgets.loc[payment_method_budgets['amount_limit'].idxmax()]
    max_budget = {'payment_method': max_payment_method['payment_method'], 'amount': float(max_payment_method['amount_limit'])}
    return (payment_method_budgets, max_budget)

def export_expense_csv(filename:str, expense_tuple:tuple) -> bool:
    '''Exports the given expense data and writes it into a csv file according to the file name
    It also returns a boolean indicating success or failure.
    args:
        filename (str): The name of the file to write to.
        expense_tuple (tuple): A tuple containing the validity of the operation and the list of expenses.
    returns:
        bool: True if the file is written successfully, False otherwise.'''
    valid,expenses = expense_tuple
    if not valid:
        return False
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'date', 'amount', 'category', 'description', 'payment_method'])
        writer.writerows(expenses)
    return True

def export_budget_csv(filename:str, budget_tuple:tuple, column_names:list) -> bool:
    '''Exports the given budget data and writes it into a csv file according to the file name and column names
    It also returns a boolean indicating success or failure.
    
    args:
        filename (str): The name of the file to write to.
        budget_tuple (tuple): A tuple containing the validity of the operation and the list of budgets.
        column_names (list): A list of strings containing the column names to be used in the csv file.
    returns:
        bool: True if the file is written successfully, False otherwise.'''
    valid,budgets = budget_tuple
    if not valid:
        return False
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(budgets)
    return True