import matplotlib.pyplot as plt
import numpy as np
from analytics import get_each_monthly_expense_year_df,get_daily_expense_month_year_df, get_category_expense_month_year_df,get_payment_method_expense_month_year_df,get_each_monthly_budget_year_df,get_category_monthly_budget_year_df,get_payment_method_monthly_budget_year_df
from constant import months
from matplotlib.figure import Figure
def bargraph_monthly_expense(year:int) -> Figure:
    ''' generates a bar graph of the monthly expense of each month for a given year and 
    also displays the maximum spending month and amount.
    args: 
        year (int): The year for which to generate the bar graph.
    returns: 
        fig (Figure): A figure object containing the bar graph.
        '''
    monthly_expenses, max_spending = get_each_monthly_expense_year_df(year)
    fig=plt.Figure(figsize=(9, 5), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    ax.bar(monthly_expenses['month'], monthly_expenses['amount'],color="#9c0909",width=0.6,edgecolor='black',linewidth=1.5)
    ax.set_xlabel('Month',fontsize=13,family='arial',fontweight='bold',color='black')#set the label of the x-axis
    ax.set_ylabel('Amount',fontsize=13,family='arial',fontweight='bold',color='black')#set the label of the y-axis
    ax.set_title(f'Monthly Expenses for {year}',fontsize=20,family='arial',fontweight='bold',color='black')#set the title of the graph
    # to display the max spending month
    ax.set_ylim(0, monthly_expenses['amount'].max() * 1.25)
    ax.annotate(
    f"Max spending month: {max_spending['month']}",
    xy=(max_spending['month'], max_spending['amount']),
    xytext=(8, 8),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->", linewidth=1.2),
    fontsize=9)
    return fig

def linegraph_daily_expense(year:int, month:int) -> Figure:
    ''' Generates a line graph of the daily expenses of a given month and year
    and also displays the maximum spending day and amount.
    args:
        year (int): The year for which to generate the line graph.
        month (int): The month for which to generate the line graph.
    returns:
        fig (Figure): A figure object containing the line graph.
    '''
    daily_expenses, max_spending = get_daily_expense_month_year_df(year, month)
    fig=plt.Figure(figsize=(9, 5), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    ax.plot(daily_expenses['day'], daily_expenses['amount'],marker='o',markersize=5,markerfacecolor="#E8C813",markeredgecolor='black',markeredgewidth=1.5,linestyle='solid',color="#f53f07",linewidth=1.7)
    ax.set_xlabel('Day',fontsize=13,family='arial',fontweight='bold',color='black')#set the label of the x-axis
    ax.set_ylabel('Amount',fontsize=13,family='arial',fontweight='bold',color='black')#set the label of the y-axis
     # map month number to month name
    ax.set_title(f'Daily Expenses for {months[month]} {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    ax.set_ylim(0, daily_expenses['amount'].max() * 1.25)
    # to display the max spending day
    ax.annotate(
    f"Max spending day: {max_spending['day']}",
    xy=(max_spending['day'], max_spending['amount']),
    xytext=(8, 8),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->", linewidth=1.2),
    fontsize=9)

    return fig


def piechart_category_expense(year:int, month:int) -> Figure:
    ''' Generates a pie chart of the category expenses of a given month and year
    also  highlights the max spending category in the pie by explode
    args:
        year (int): The year for which to generate the pie chart.
        month (int): The month for which to generate the pie chart.
    returns:
        fig (Figure): A figure object containing the pie chart.
    '''
    category_expenses, max_spending = get_category_expense_month_year_df(year, month)
    fig = plt.Figure(figsize=(7, 7), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    category_expenses = category_expenses.sort_values(by='amount', ascending=False)
    colors=["#21940a","#f5076a","#09929c",'#f53f07','#e8c813']
    explode=[0.1 if max_spending['category'] == category else 0 for category in category_expenses['category']]
    ax.pie(category_expenses['amount'], labels=category_expenses['category'], autopct='%1.1f%%',explode=explode,shadow=True,colors=colors,wedgeprops={'linewidth': 1.5, 'edgecolor': 'black'},textprops={'fontsize': 12,'color':'black','family':'arial','fontweight':'bold'},radius=1.1,center=(0, 0),pctdistance=0.8,labeldistance=1.1)
    ax.set_title(f'Category Expenses for {months[month]} {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    fig.tight_layout()
    return fig
    
def piechart_payment_method_expense(year:int, month:int) -> Figure:
    ''' Generates a pie chart of the payment method expenses of a given month and year
    also  highlights the max spending payment method in the pie by explode
    args:
        year (int): The year for which to generate the pie chart.
        month (int): The month for which to generate the pie chart.
    returns:
        fig (Figure): A figure object containing the pie chart.'''
    payment_method_expenses, max_spending = get_payment_method_expense_month_year_df(year, month)
    fig=plt.Figure(figsize=(7, 7), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    payment_method_expenses = payment_method_expenses.sort_values(by='amount', ascending=False)
    explode=[0.1 if max_spending['payment_method'] == payment_method else 0 for payment_method in payment_method_expenses['payment_method']]
    colors=["#21940a","#f5076a","#09929c",'#f53f07','#e8c813']
    ax.pie(payment_method_expenses['amount'], labels=payment_method_expenses['payment_method'], autopct='%1.1f%%',explode=explode,shadow=True,colors=colors,wedgeprops={'linewidth': 1.5, 'edgecolor': 'black'},textprops={'fontsize': 12,'color':'black','family':'arial','fontweight':'bold'},radius=1.1,center=(0, 0),pctdistance=0.8,labeldistance=1.1,startangle=90)
    ax.set_title(f'Payment Method Expenses for {months[month]} {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    fig.tight_layout()
    return fig

def double_bar_graph_monthly_budget(year:int) -> Figure:
    ''' Generates a double bar graph of the monthly budget and expenses of a given year 
    args: 
        year (int): The year for which to generate the double bar graph.
    returns:    
        fig (Figure): A figure object containing the double bar graph.'''
    monthly_budget, max_budget = get_each_monthly_budget_year_df(year)
    monthly_expenses, max_spending = get_each_monthly_expense_year_df(year)
    # set the position of the xticks
    x = np.arange(len(monthly_budget['month']))
    # set the size of the figure
    fig=plt.Figure(figsize=(10, 6), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    ax.bar(x - 0.2, monthly_budget['amount_limit'], label='Budget',color="#fd7e08",width=0.4,edgecolor='black',linewidth=1.5)
    ax.bar(x + 0.2, monthly_expenses['amount'], label='Expenses',color="#9c0909",width=0.4,edgecolor='black',linewidth=1.5)
    ax.set_xlabel('Month',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_ylabel('Amount',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_xticks(x, monthly_budget['month']) # to set the position of the xticks
    ax.set_xticklabels(monthly_budget['month'],fontsize=10,family='arial',fontweight='bold',color='black')# to set the label of the xticks
    ax.set_title(f'Monthly Budget and Expenses for {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    # to specify the label for each bar
    ax.legend()
    fig.tight_layout()
    return fig

def double_bar_graph_category_budget(year:int,month:int) -> Figure:
    ''' Generates a double bar graph of the category budget and expenses of a given month and year 
    args: 
        year (int): The year for which to generate the double bar graph.
        month (int): The month for which to generate the double bar graph.
    returns:    
        fig (Figure): A figure object containing the double bar graph.'''
    category_budget, max_budget = get_category_monthly_budget_year_df(year,month)
    category_expenses, max_spending = get_category_expense_month_year_df(year,month)
    # set the position of the xticks
    x = np.arange(len(category_budget['category']))
    # set the size of the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.bar(x - 0.2, category_budget['amount_limit'], label='Budget',color="#0c5213",width=0.4,edgecolor='black',linewidth=1.5)
    ax.bar(x + 0.2, category_expenses['amount'], label='Expenses',color="#00fa2a",width=0.4,edgecolor='black',linewidth=1.5)
    ax.set_xlabel('Category',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_ylabel('Amount',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_xticks(x, category_budget['category']) # to set the position of the xticks
    ax.set_xticklabels(category_budget['category'],fontsize=10,family='arial',fontweight='bold',color='black')# to set the label of the xticks
    ax.set_title(f'Category Budget and Expenses for {months[month]} {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    # to specify the label for each bar
    ax.legend()
    fig.tight_layout()
    return fig

def double_bar_graph_payment_method_budget(year:int,month:int) -> Figure:
    ''' Generates a double bar graph of the payment method budget and expenses of a given month and year 
    args: 
        year (int): The year for which to generate the double bar graph.
        month (int): The month for which to generate the double bar graph.
    returns:    
        fig (Figure): A figure object containing the double bar graph.'''
    payment_method_budget, max_budget = get_payment_method_monthly_budget_year_df(year,month)
    payment_method_expenses, max_spending = get_payment_method_expense_month_year_df(year,month)
    # set the position of the xticks
    x = np.arange(len(payment_method_budget['payment_method']))
    # set the size of the figure
    fig=plt.Figure(figsize=(10, 6), dpi=100) # set the size of the figure and create a figure object
    ax = fig.add_subplot(111)
    ax.bar(x - 0.2, payment_method_budget['amount_limit'], label='Budget',color="#111A66",width=0.4,edgecolor='black',linewidth=1.5)
    ax.bar(x + 0.2, payment_method_expenses['amount'], label='Expenses',color="#04f7ea",width=0.4,edgecolor='black',linewidth=1.5)
    ax.set_xlabel('Payment Method',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_ylabel('Amount',fontsize=13,family='arial',fontweight='bold',color='black')
    ax.set_xticks(x, payment_method_budget['payment_method']) # to set the position of the xticks
    ax.set_xticklabels(payment_method_budget['payment_method'],fontsize=10,family='arial',fontweight='bold',color='black')# to set the label of the xticks
    ax.set_title(f'Payment Method Budget and Expenses for {months[month]} {year}',fontsize=20,family='arial',fontweight='bold',color='black')
    # to specify the label for each bar
    ax.legend()
    fig.tight_layout()
    return fig

"""bargraph_monthly_expense(2024)
linegraph_daily_expense(2024,1)
piechart_category_expense(2024,1)
piechart_payment_method_expense(2024,1)
double_bar_graph_monthly_budget(2024)
double_bar_graph_category_budget(2024,3)
double_bar_graph_payment_method_budget(2024,3)"""