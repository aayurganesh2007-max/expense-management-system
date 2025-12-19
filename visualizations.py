import matplotlib.pyplot as plt
from analytics import get_each_monthly_expense_year_df,get_daily_expense_month_year_df, get_category_expense_month_year_df,get_payment_method_expense_month_year_df,get_each_monthly_budget_year_df,get_category_monthly_budget_year_df,get_payment_method_monthly_budget_year_df
def bargraph_monthly_expense(year:int) -> dict:
    ''' generates a bar graph of the monthly expense of each month for a given year and 
    also returns the maximum spending month and amount.
    args: 
        year (int): The year for which to generate the bar graph.
    returns:    
        dict: A tuple containing the maximum spending month and amount.'''
    monthly_expenses, max_spending = get_each_monthly_expense_year_df(year)
    plt.figure(figsize=(7, 3)) # set the size of the figure
    plt.bar(monthly_expenses['month'], monthly_expenses['amount'])
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title(f'Monthly Expenses for {year}')
    plt.tight_layout()
    plt.show()
    return max_spending

def linegraph_daily_expense(year:int, month:int) -> dict:
    ''' Generates a line graph of the daily expenses of a given month and year
    and also returns the maximum spending day and amount.
    args:
        year (int): The year for which to generate the line graph.
        month (int): The month for which to generate the line graph.
    returns:
        dict: A tuple containing the maximum spending day and amount.'''
    daily_expenses, max_spending = get_daily_expense_month_year_df(year, month)
    plt.figure(figsize=(10, 6)) # set the size of the figure
    plt.plot(daily_expenses['day'], daily_expenses['amount'])
    plt.xlabel('Day')
    plt.ylabel('Amount')
    plt.title(f'Daily Expenses for {month} {year}')
    plt.tight_layout()
    plt.show()
    return max_spending

def piechart_category_expense(year:int, month:int) -> dict:
    ''' Generates a pie chart of the category expenses of a given month and year
    also  highlights the max spending category in the pie by explode
    and also returns the maximum spent category and amount.
    args:
        year (int): The year for which to generate the pie chart.
        month (int): The month for which to generate the pie chart.
    returns:
        dict: A tuple containing the maximum spent category and amount.'''
    category_expenses, max_spending = get_category_expense_month_year_df(year, month)
    plt.figure(figsize=(8, 8)) # set the size of the figure
    category_expenses = category_expenses.sort_values(by='amount', ascending=False)
    explode=[0.1 if max_spending['category'] == category else 0 for category in category_expenses['category']]
    plt.pie(category_expenses['amount'], labels=category_expenses['category'], autopct='%1.1f%%',explode=explode)
    plt.title(f'Category Expenses for {month} {year}')
    plt.tight_layout()
    plt.show()
    return max_spending
    
def piechart_payment_method_expense(year:int, month:int) -> dict:
    ''' Generates a pie chart of the payment method expenses of a given month and year
    also  highlights the max spending payment method in the pie by explode
    and also returns the maximum spent payment method and amount.
    args:
        year (int): The year for which to generate the pie chart.
        month (int): The month for which to generate the pie chart.
    returns:
        dict: A tuple containing the maximum spent payment method and amount.'''
    payment_method_expenses, max_spending = get_payment_method_expense_month_year_df(year, month)
    plt.figure(figsize=(8, 8)) # set the size of the figure
    payment_method_expenses = payment_method_expenses.sort_values(by='amount', ascending=False)
    explode=[0.1 if max_spending['payment_method'] == payment_method else 0 for payment_method in payment_method_expenses['payment_method']]
    plt.pie(payment_method_expenses['amount'], labels=payment_method_expenses['payment_method'], autopct='%1.1f%%',explode=explode)
    plt.title(f'Payment Method Expenses for {month} {year}')
    plt.tight_layout()
    plt.show()
    return max_spending

def double_bar_graph_monthly_budget(year:int) -> None:
    ''' Generates a double bar graph of the monthly budget and expenses of a given year 
    args: 
        year (int): The year for which to generate the double bar graph.
    returns:    
        None'''
    monthly_budget, monthly_expenses = get_each_monthly_budget_year_df(year)
    plt.figure(figsize=(10, 6)) # set the size of the figure
    plt.bar(monthly_budget['month'], monthly_budget['amount'], label='Budget')
    plt.bar(monthly_expenses['month'], monthly_expenses['amount'], label='Expenses')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title(f'Monthly Budget and Expenses for {year}')
    # to specify the label for each bar
    plt.legend()
    plt.tight_layout()
    plt.show()

def double_bar_graph_category_budget(year:int,month:int) -> None:
    ''' Generates a double bar graph of the category budget and expenses of a given month and year 
    args: 
        year (int): The year for which to generate the double bar graph.
        month (int): The month for which to generate the double bar graph.
    returns:    
        None'''
    category_budget, category_expenses = get_category_monthly_budget_year_df(year,month)
    plt.figure(figsize=(10, 6)) # set the size of the figure
    plt.bar(category_budget['category'], category_budget['amount'], label='Budget')
    plt.bar(category_expenses['category'], category_expenses['amount'], label='Expenses')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title(f'Category Budget and Expenses for {month} {year}')
    # to specify the label for each bar
    plt.legend()
    plt.tight_layout()
    plt.show()

def double_bar_graph_payment_method_budget(year:int,month:int) -> None:
    ''' Generates a double bar graph of the payment method budget and expenses of a given month and year 
    args: 
        year (int): The year for which to generate the double bar graph.
        month (int): The month for which to generate the double bar graph.
    returns:    
        None'''
    payment_method_budget, payment_method_expenses = get_payment_method_monthly_budget_year_df(year,month)
    plt.figure(figsize=(10, 6)) # set the size of the figure
    plt.bar(payment_method_budget['payment_method'], payment_method_budget['amount'], label='Budget')
    plt.bar(payment_method_expenses['payment_method'], payment_method_expenses['amount'], label='Expenses')
    plt.xlabel('Payment Method')
    plt.ylabel('Amount')
    plt.title(f'Payment Method Budget and Expenses for {month} {year}')
    # to specify the label for each bar
    plt.legend()
    plt.tight_layout()
    plt.show()

bargraph_monthly_expense(2024)