import tkinter as tk
from tkinter import ttk, messagebox
from expense_gui import clear_content
from visualizations import bargraph_monthly_expense,linegraph_daily_expense,piechart_category_expense,piechart_payment_method_expense,double_bar_graph_monthly_budget,double_bar_graph_category_budget,double_bar_graph_payment_method_budget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from validators import valid_year_in_database,valid_year_month_in_database
from constant import months
def open_visualizations_window(window):
    '''Function to open the visualizations management window and operate on this window with different frames and widgets.
    args:
        window: the main window
    returns:
        None'''
    #   creating a new window for the visualizations
    new_viz_window = tk.Toplevel(window)
    new_viz_window.title("Visualizations Management")
    new_viz_window.geometry("800x700")
    new_viz_window.grid_rowconfigure(0, weight=1)
    new_viz_window.grid_columnconfigure(1, weight=3)
    #creating a new frame for the side bar with butttons
    viz_frame = tk.Frame(new_viz_window, padx=10, pady=10, bg="#9c0b0b",relief="raised",bd=5)
    viz_frame.grid(row=0, column=0, sticky="nsew")
    viz_frame.grid_columnconfigure(0, weight=1)
    #creating a new main content frame for better layout management
    viz_content_frame = tk.Frame(new_viz_window, padx=10, pady=10, bg="#c01010")
    viz_content_frame.grid(row=0, column=1, sticky="nsew")
    viz_content_frame.grid_columnconfigure(0, weight=1)
    viz_content_frame.grid_rowconfigure(0, weight=1)
    #button for entering new visualization
    viz_bargraph_monthly_expense_btn = tk.Button(viz_frame, text="Bar Graph \nMonthly Expense", font=("Arial", 15, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_bargraph_monthly_expense(viz_content_frame))
    viz_bargraph_monthly_expense_btn.grid(row=0, column=0, pady=(10,0))

    viz_linegraph_daily_expense_btn = tk.Button(viz_frame, text="Line Graph \nDaily Expense", font=("Arial", 15, "bold"), bg="#e38c0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_linegraph_daily_expense(viz_content_frame))
    viz_linegraph_daily_expense_btn.grid(row=1, column=0, pady=(10,0))

    viz_piechart_category_expense_btn = tk.Button(viz_frame, text="Pie Chart \nCategory Expense", font=("Arial", 15, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_piechart_category_expense(viz_content_frame))
    viz_piechart_category_expense_btn.grid(row=2, column=0, pady=(10,0))

    viz_piechart_payment_method_expense_btn = tk.Button(viz_frame, text="Pie Chart \nPayment Method Expense", font=("Arial", 15, "bold"), bg="#e38c0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_piechart_payment_method_expense(viz_content_frame))
    viz_piechart_payment_method_expense_btn.grid(row=3, column=0, pady=(10,0))

    viz_double_bar_graph_monthly_budget_btn = tk.Button(viz_frame, text="Double Bar Graph \nMonthly Budget", font=("Arial", 15, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_double_bar_graph_monthly_budget(viz_content_frame))
    viz_double_bar_graph_monthly_budget_btn.grid(row=4, column=0, pady=(10,0))

    viz_double_bar_graph_category_budget_btn = tk.Button(viz_frame, text="Double Bar Graph \nCategory Budget", font=("Arial", 15, "bold"), bg="#e38c0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_double_bar_graph_category_budget(viz_content_frame))
    viz_double_bar_graph_category_budget_btn.grid(row=5, column=0, pady=(10,0))

    viz_double_bar_graph_payment_method_budget_btn = tk.Button(viz_frame, text="Double Bar Graph \nPayment Method Budget", font=("Arial", 15, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command= lambda:viz_double_bar_graph_payment_method_budget(viz_content_frame))
    viz_double_bar_graph_payment_method_budget_btn.grid(row=6, column=0, pady=(10,0))

def viz_bargraph_monthly_expense(viz_content_frame):
    '''Function to open the bar graph of monthly expenses from the database by creating a new frame in the same window when called.
    It takes the year form user input and displays the bar graph of monthly expenses, after validating the year exists in the database.
    args:
        viz_content_frame: The frame where the bar graph of monthly expenses frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the bar graph of monthly expenses frame
    clear_content(viz_content_frame)
    viz_bargraph_monthly_expense_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_bargraph_monthly_expense_frame.grid(row=0, column=0, sticky="nsew")
    viz_bargraph_monthly_expense_frame.grid_columnconfigure(0, weight=1)

    viz_bargraph_monthly_expense_lbl = tk.Label(viz_bargraph_monthly_expense_frame, text="Bar Graph \nMonthly Expense", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_bargraph_monthly_expense_lbl.grid(row=0, column=0,pady=(10,0))

    viz_bargraph_monthly_expense_year_lbl = tk.Label(viz_bargraph_monthly_expense_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_bargraph_monthly_expense_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_bargraph_monthly_expense_year_entry = tk.Entry(viz_bargraph_monthly_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_bargraph_monthly_expense_year_entry.grid(row=2, column=0, pady=(6,0))

    def submit_viz_bargraph_monthly_expense():
        '''Function to submit the bar graph of monthly expenses from the database when called.
        It takes the year form user input and displays the bar graph of monthly expenses, after validating the year exists in the database.
        args:
            None
        returns:    
            None'''
        year = viz_bargraph_monthly_expense_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_in_database(year,"expense.db","expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        clear_content(viz_bargraph_monthly_expense_frame)#clear the content of the frame
        viz_bargraph_monthly_expense_fig_frame = tk.Frame(viz_bargraph_monthly_expense_frame, padx=10, pady=10, bg="#c01010")
        viz_bargraph_monthly_expense_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_bargraph_monthly_expense_fig_frame.grid_columnconfigure(0, weight=1)
        viz_bargraph_monthly_expensefig = bargraph_monthly_expense(year)
        viz_bargraph_monthly_expensefig_canvas = FigureCanvasTkAgg(viz_bargraph_monthly_expensefig, master=viz_bargraph_monthly_expense_fig_frame)
        viz_bargraph_monthly_expensefig_canvas.draw()
        viz_bargraph_monthly_expensefig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_bargraph_monthly_expense_diplay_btn = tk.Button(viz_bargraph_monthly_expense_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_bargraph_monthly_expense)
    viz_bargraph_monthly_expense_diplay_btn.grid(row=3, column=0, pady=(10,0))
    
def viz_linegraph_daily_expense(viz_content_frame):
    '''Function to open the line graph of daily expenses from the database by creating a new frame in the same window when called.
    It takes the year form user input and displays the line graph of daily expenses, after validating the year exists in the database.
    args:
        viz_content_frame: The frame where the line graph of daily expenses frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the line graph of daily expenses frame
    clear_content(viz_content_frame)
    viz_linegraph_daily_expense_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_linegraph_daily_expense_frame.grid(row=0, column=0, sticky="nsew")
    viz_linegraph_daily_expense_frame.grid_columnconfigure(0, weight=1)

    viz_linegraph_daily_expense_lbl = tk.Label(viz_linegraph_daily_expense_frame, text="Line Graph \nDaily Expense", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_linegraph_daily_expense_lbl.grid(row=0, column=0,pady=(10,0))

    viz_linegraph_daily_expense_year_lbl = tk.Label(viz_linegraph_daily_expense_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_linegraph_daily_expense_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_linegraph_daily_expense_year_entry = tk.Entry(viz_linegraph_daily_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_linegraph_daily_expense_year_entry.grid(row=2, column=0, pady=(6,0))

    viz_linegraph_daily_expense_month_lbl = tk.Label(viz_linegraph_daily_expense_frame, text="Month:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_linegraph_daily_expense_month_lbl.grid(row=3, column=0, pady=(20,0))
    #combobox for selecting the month in text jan to dec
    viz_linegraph_daily_expense_month_entry = ttk.Combobox(viz_linegraph_daily_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_linegraph_daily_expense_month_entry['values'] = list(months.values())
    viz_linegraph_daily_expense_month_entry.grid(row=4, column=0, pady=(6,0))    

    def submit_viz_linegraph_daily_expense():
        """Function to submit the line graph of daily expenses from the database when called.
        It takes the year and month form user input and displays the line graph of daily expenses, after validating the year and month exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_linegraph_daily_expense_year_entry.get()
        for month,value in months.items():
            if value == viz_linegraph_daily_expense_month_entry.get():
                break
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_month_in_database(year, month, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year and month.")
            return
        clear_content(viz_linegraph_daily_expense_frame)#clear the content of the frame
        viz_linegraph_daily_expense_fig_frame = tk.Frame(viz_linegraph_daily_expense_frame, padx=10, pady=10, bg="#c01010")
        viz_linegraph_daily_expense_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_linegraph_daily_expense_fig_frame.grid_columnconfigure(0, weight=1)
        viz_linegraph_daily_expensefig = linegraph_daily_expense(year, month)
        viz_linegraph_daily_expensefig_canvas = FigureCanvasTkAgg(viz_linegraph_daily_expensefig, master=viz_linegraph_daily_expense_fig_frame)
        viz_linegraph_daily_expensefig_canvas.draw()
        viz_linegraph_daily_expensefig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
    viz_linegraph_daily_expense_diplay_btn = tk.Button(viz_linegraph_daily_expense_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_linegraph_daily_expense)
    viz_linegraph_daily_expense_diplay_btn.grid(row=5, column=0, pady=(10,0))

def viz_piechart_category_expense(viz_content_frame):
    '''Function to open the pie chart of category expenses from the database by creating a new frame in the same window when called.
    It takes the year and month from user input and displays the pie chart of category expenses, after validating the year and month exists in the database.
    args:
        viz_content_frame: The frame where the pie chart of category expenses frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the pie chart of category expenses frame
    clear_content(viz_content_frame)
    viz_piechart_category_expense_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_piechart_category_expense_frame.grid(row=0, column=0, sticky="nsew")
    viz_piechart_category_expense_frame.grid_columnconfigure(0, weight=1)

    viz_piechart_category_expense_lbl = tk.Label(viz_piechart_category_expense_frame, text="Pie Chart \nCategory Expense", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_piechart_category_expense_lbl.grid(row=0, column=0,pady=(10,0))

    viz_piechart_category_expense_year_lbl = tk.Label(viz_piechart_category_expense_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_piechart_category_expense_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_piechart_category_expense_year_entry = tk.Entry(viz_piechart_category_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_piechart_category_expense_year_entry.grid(row=2, column=0, pady=(6,0))

    viz_piechart_category_expense_month_lbl = tk.Label(viz_piechart_category_expense_frame, text="Month:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_piechart_category_expense_month_lbl.grid(row=3, column=0, pady=(20,0))
    #combobox for selecting the month in text jan to dec
    viz_piechart_category_expense_month_entry = ttk.Combobox(viz_piechart_category_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_piechart_category_expense_month_entry['values'] = list(months.values())
    viz_piechart_category_expense_month_entry.grid(row=4, column=0, pady=(6,0))    

    def submit_viz_piechart_category_expense():
        """Function to submit the pie chart of category expenses from the database when called.
        It takes the year and month form user input and displays the pie chart of category expenses, after validating the year and month exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_piechart_category_expense_year_entry.get()
        for month,value in months.items():
            if value == viz_piechart_category_expense_month_entry.get():
                break
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_month_in_database(year, month, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year and month.")
            return
        clear_content(viz_piechart_category_expense_frame)#clear the content of the frame
        viz_piechart_category_expense_fig_frame = tk.Frame(viz_piechart_category_expense_frame, padx=10, pady=10, bg="#c01010")
        viz_piechart_category_expense_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_piechart_category_expense_fig_frame.grid_columnconfigure(0, weight=1)
        viz_piechart_category_expensefig = piechart_category_expense(year, month)
        viz_piechart_category_expensefig_canvas = FigureCanvasTkAgg(viz_piechart_category_expensefig, master=viz_piechart_category_expense_fig_frame)
        viz_piechart_category_expensefig_canvas.draw()
        viz_piechart_category_expensefig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_piechart_category_expense_diplay_btn = tk.Button(viz_piechart_category_expense_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_piechart_category_expense)
    viz_piechart_category_expense_diplay_btn.grid(row=5, column=0, pady=(10,0))

def viz_piechart_payment_method_expense(viz_content_frame):
    '''Function to open the pie chart of payment method expenses from the database by creating a new frame in the same window when called.
    It takes the year and month from user input and displays the pie chart of payment method expenses, after validating the year and month exists in the database.
    args:
        viz_content_frame: The frame where the pie chart of payment method expenses frame will be created.        
    returns:    
        None'''
    #clear existing frames before opening the pie chart of payment method expenses frame
    clear_content(viz_content_frame)
    viz_piechart_payment_method_expense_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_piechart_payment_method_expense_frame.grid(row=0, column=0, sticky="nsew")
    viz_piechart_payment_method_expense_frame.grid_columnconfigure(0, weight=1)

    viz_piechart_payment_method_expense_lbl = tk.Label(viz_piechart_payment_method_expense_frame, text="Pie Chart \nPayment Method Expense", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_piechart_payment_method_expense_lbl.grid(row=0, column=0,pady=(10,0))

    viz_piechart_payment_method_expense_year_lbl = tk.Label(viz_piechart_payment_method_expense_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")        
    viz_piechart_payment_method_expense_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_piechart_payment_method_expense_year_entry = tk.Entry(viz_piechart_payment_method_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_piechart_payment_method_expense_year_entry.grid(row=2, column=0, pady=(6,0))

    viz_piechart_payment_method_expense_month_lbl = tk.Label(viz_piechart_payment_method_expense_frame, text="Month:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_piechart_payment_method_expense_month_lbl.grid(row=3, column=0, pady=(20,0))
    #combobox for selecting the month in text jan to dec
    viz_piechart_payment_method_expense_month_entry = ttk.Combobox(viz_piechart_payment_method_expense_frame, width=4, font=("Arial", 16), justify="center")
    viz_piechart_payment_method_expense_month_entry['values'] = list(months.values())
    viz_piechart_payment_method_expense_month_entry.grid(row=4, column=0, pady=(6,0))    

    def submit_viz_piechart_payment_method_expense():
        """Function to submit the pie chart of payment method expenses from the database when called.
        It takes the year and month form user input and displays the pie chart of payment method expenses, after validating the year and month exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_piechart_payment_method_expense_year_entry.get()
        for month,value in months.items():
            if value == viz_piechart_payment_method_expense_month_entry.get():
                break
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_month_in_database(year, month, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year and month.")
            return
        clear_content(viz_piechart_payment_method_expense_frame)#clear the content of the frame
        viz_piechart_payment_method_expense_fig_frame = tk.Frame(viz_piechart_payment_method_expense_frame, padx=10, pady=10, bg="#c01010")
        viz_piechart_payment_method_expense_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_piechart_payment_method_expense_fig_frame.grid_columnconfigure(0, weight=1)
        viz_piechart_payment_method_expensefig = piechart_payment_method_expense(year, month)
        viz_piechart_payment_method_expensefig_canvas = FigureCanvasTkAgg(viz_piechart_payment_method_expensefig, master=viz_piechart_payment_method_expense_fig_frame)
        viz_piechart_payment_method_expensefig_canvas.draw()
        viz_piechart_payment_method_expensefig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_piechart_payment_method_expense_diplay_btn = tk.Button(viz_piechart_payment_method_expense_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_piechart_payment_method_expense)
    viz_piechart_payment_method_expense_diplay_btn.grid(row=5, column=0, pady=(10,0))

def viz_double_bar_graph_monthly_budget(viz_content_frame):
    '''Function to open the double bar graph of monthly budget from the database by creating a new frame in the same window when called.
    It takes the year from user input and displays the double bar graph of monthly budget, after validating the year exists in the database.
    args:
        viz_content_frame: The frame where the double bar graph of monthly budget frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the double bar graph of monthly budget frame
    clear_content(viz_content_frame)
    viz_double_bar_graph_monthly_budget_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_double_bar_graph_monthly_budget_frame.grid(row=0, column=0, sticky="nsew")
    viz_double_bar_graph_monthly_budget_frame.grid_columnconfigure(0, weight=1)

    viz_double_bar_graph_monthly_budget_lbl = tk.Label(viz_double_bar_graph_monthly_budget_frame, text="Double Bar Graph \nMonthly Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_double_bar_graph_monthly_budget_lbl.grid(row=0, column=0,pady=(10,0))

    viz_double_bar_graph_monthly_budget_year_lbl = tk.Label(viz_double_bar_graph_monthly_budget_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_double_bar_graph_monthly_budget_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_double_bar_graph_monthly_budget_year_entry = tk.Entry(viz_double_bar_graph_monthly_budget_frame, width=4, font=("Arial", 16), justify="center")
    viz_double_bar_graph_monthly_budget_year_entry.grid(row=2, column=0, pady=(6,0))

    def submit_viz_double_bar_graph_monthly_budget():
        """Function to submit the double bar graph of monthly budget from the database when called.
        It takes the year form user input and displays the double bar graph of monthly budget, after validating the year exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_double_bar_graph_monthly_budget_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_in_database(year, "budget.db", "monthly_budget") and not valid_year_in_database(year, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        clear_content(viz_double_bar_graph_monthly_budget_frame)#clear the content of the frame
        viz_double_bar_graph_monthly_budget_fig_frame = tk.Frame(viz_double_bar_graph_monthly_budget_frame, padx=10, pady=10, bg="#c01010")
        viz_double_bar_graph_monthly_budget_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_double_bar_graph_monthly_budget_fig_frame.grid_columnconfigure(0, weight=1)
        viz_double_bar_graph_monthly_budgetfig = double_bar_graph_monthly_budget(year)
        viz_double_bar_graph_monthly_budgetfig_canvas = FigureCanvasTkAgg(viz_double_bar_graph_monthly_budgetfig, master=viz_double_bar_graph_monthly_budget_fig_frame)
        viz_double_bar_graph_monthly_budgetfig_canvas.draw()
        viz_double_bar_graph_monthly_budgetfig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_double_bar_graph_monthly_budget_diplay_btn = tk.Button(viz_double_bar_graph_monthly_budget_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_double_bar_graph_monthly_budget)
    viz_double_bar_graph_monthly_budget_diplay_btn.grid(row=3, column=0, pady=(10,0))

def viz_double_bar_graph_category_budget(viz_content_frame):
    '''Function to open the double bar graph of category budget from the database by creating a new frame in the same window when called.
    It takes the year and month from user input and displays the double bar graph of category budget, after validating the year and month exists in the database.
    args:
        viz_content_frame: The frame where the double bar graph of category budget frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the double bar graph of category budget frame
    clear_content(viz_content_frame)
    viz_double_bar_graph_category_budget_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_double_bar_graph_category_budget_frame.grid(row=0, column=0, sticky="nsew")
    viz_double_bar_graph_category_budget_frame.grid_columnconfigure(0, weight=1)

    viz_double_bar_graph_category_budget_lbl = tk.Label(viz_double_bar_graph_category_budget_frame, text="Double Bar Graph \nCategory Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_double_bar_graph_category_budget_lbl.grid(row=0, column=0,pady=(10,0))

    viz_double_bar_graph_category_budget_year_lbl = tk.Label(viz_double_bar_graph_category_budget_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_double_bar_graph_category_budget_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_double_bar_graph_category_budget_year_entry = tk.Entry(viz_double_bar_graph_category_budget_frame, width=4, font=("Arial", 16), justify="center")
    viz_double_bar_graph_category_budget_year_entry.grid(row=2, column=0, pady=(6,0))

    viz_double_bar_graph_category_budget_month_lbl = tk.Label(viz_double_bar_graph_category_budget_frame, text="Month:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_double_bar_graph_category_budget_month_lbl.grid(row=3, column=0, pady=(20,0))
    #combobox for selecting the month in text jan to dec
    viz_double_bar_graph_category_budget_month_entry = ttk.Combobox(viz_double_bar_graph_category_budget_frame, width=4, font=("Arial", 16), justify="center")
    viz_double_bar_graph_category_budget_month_entry['values'] = list(months.values())
    viz_double_bar_graph_category_budget_month_entry.grid(row=4, column=0, pady=(6,0))    

    def submit_viz_double_bar_graph_category_budget():
        """Function to submit the double bar graph of category budget from the database when called.
        It takes the year and month form user input and displays the double bar graph of category budget, after validating the year and month exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_double_bar_graph_category_budget_year_entry.get()
        for month,value in months.items():
            if value == viz_double_bar_graph_category_budget_month_entry.get():
                break
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_month_in_database(year, month, "budget.db", "monthly_category_budget") and not valid_year_month_in_database(year, month, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year and month.")
            return
        clear_content(viz_double_bar_graph_category_budget_frame)#clear the content of the frame
        viz_double_bar_graph_category_budget_fig_frame = tk.Frame(viz_double_bar_graph_category_budget_frame, padx=10, pady=10, bg="#c01010")
        viz_double_bar_graph_category_budget_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_double_bar_graph_category_budget_fig_frame.grid_columnconfigure(0, weight=1)
        viz_double_bar_graph_category_budgetfig = double_bar_graph_category_budget(year,month)
        viz_double_bar_graph_category_budgetfig_canvas = FigureCanvasTkAgg(viz_double_bar_graph_category_budgetfig, master=viz_double_bar_graph_category_budget_fig_frame)
        viz_double_bar_graph_category_budgetfig_canvas.draw()
        viz_double_bar_graph_category_budgetfig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_double_bar_graph_category_budget_diplay_btn = tk.Button(viz_double_bar_graph_category_budget_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_double_bar_graph_category_budget)
    viz_double_bar_graph_category_budget_diplay_btn.grid(row=5, column=0, pady=(10,0))

def viz_double_bar_graph_payment_method_budget(viz_content_frame):
    '''Function to open the double bar graph of payment method budget from the database by creating a new frame in the same window when called.
    It takes the year and month from user input and displays the double bar graph of payment method budget, after validating the year and month exists in the database.
    args:
        viz_content_frame: The frame where the double bar graph of payment method budget frame will be created.
    returns:    
        None'''
    #clear existing frames before opening the double bar graph of payment method budget frame
    clear_content(viz_content_frame)
    viz_double_bar_graph_payment_method_budget_frame = tk.Frame(viz_content_frame, padx=10, pady=10, bg="#c01010")
    viz_double_bar_graph_payment_method_budget_frame.grid(row=0, column=0, sticky="nsew")
    viz_double_bar_graph_payment_method_budget_frame.grid_columnconfigure(0, weight=1)

    viz_double_bar_graph_payment_method_budget_lbl = tk.Label(viz_double_bar_graph_payment_method_budget_frame, text="Double Bar Graph \nPayment Method Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    viz_double_bar_graph_payment_method_budget_lbl.grid(row=0, column=0,pady=(10,0))

    viz_double_bar_graph_payment_method_budget_year_lbl = tk.Label(viz_double_bar_graph_payment_method_budget_frame, text="Year:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_double_bar_graph_payment_method_budget_year_lbl.grid(row=1, column=0, pady=(20,0))
    viz_double_bar_graph_payment_method_budget_year_entry = tk.Entry(viz_double_bar_graph_payment_method_budget_frame, width=4, font=("Arial", 16), justify="center")    
    viz_double_bar_graph_payment_method_budget_year_entry.grid(row=2, column=0, pady=(6,0))

    viz_double_bar_graph_payment_method_budget_month_lbl = tk.Label(viz_double_bar_graph_payment_method_budget_frame, text="Month:", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
    viz_double_bar_graph_payment_method_budget_month_lbl.grid(row=3, column=0, pady=(20,0))
    #combobox for selecting the month in text jan to dec
    viz_double_bar_graph_payment_method_budget_month_entry = ttk.Combobox(viz_double_bar_graph_payment_method_budget_frame, width=4, font=("Arial", 16), justify="center")
    viz_double_bar_graph_payment_method_budget_month_entry['values'] = list(months.values())
    viz_double_bar_graph_payment_method_budget_month_entry.grid(row=4, column=0, pady=(6,0))    

    def submit_viz_double_bar_graph_payment_method_budget():
        """Function to submit the double bar graph of payment method budget from the database when called.
        It takes the year and month form user input and displays the double bar graph of payment method budget, after validating the year and month exists in the database.
        args:
            None
        returns:    
            None"""
        year = viz_double_bar_graph_payment_method_budget_year_entry.get()
        for month,value in months.items():
            if value == viz_double_bar_graph_payment_method_budget_month_entry.get():
                break
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        if not valid_year_month_in_database(year, month, "budget.db", "monthly_payment_method_budget") and not valid_year_month_in_database(year, month, "expense.db", "expenses"):
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year and month.")
            return
        clear_content(viz_double_bar_graph_payment_method_budget_frame)#clear the content of the frame
        viz_double_bar_graph_payment_method_budget_fig_frame = tk.Frame(viz_double_bar_graph_payment_method_budget_frame, padx=10, pady=10, bg="#c01010")
        viz_double_bar_graph_payment_method_budget_fig_frame.grid(row=0, column=0, sticky="nsew")
        viz_double_bar_graph_payment_method_budget_fig_frame.grid_columnconfigure(0, weight=1)
        viz_double_bar_graph_payment_method_budgetfig = double_bar_graph_payment_method_budget(year,month)
        viz_double_bar_graph_payment_method_budgetfig_canvas = FigureCanvasTkAgg(viz_double_bar_graph_payment_method_budgetfig, master=viz_double_bar_graph_payment_method_budget_fig_frame)
        viz_double_bar_graph_payment_method_budgetfig_canvas.draw()
        viz_double_bar_graph_payment_method_budgetfig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    viz_double_bar_graph_payment_method_budget_diplay_btn = tk.Button(viz_double_bar_graph_payment_method_budget_frame, text="Display", font=("Arial", 20, "bold"), bg="#e94c0e", fg="black", bd=6, relief="raised", justify="center", command=submit_viz_double_bar_graph_payment_method_budget)
    viz_double_bar_graph_payment_method_budget_diplay_btn.grid(row=5, column=0, pady=(10,0))     
