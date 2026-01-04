import tkinter as tk
import os
from tkinter import ttk, messagebox,filedialog
from expense_gui import clear_content, save_file_dialogue
from budget import get_all_budgets, get_all_category_budgets, get_all_payment_method_budgets, delete_budget_limit, set_update_monthly_budget, set_update_monthly_category_budget, set_update_monthly_payment_method_budget
from constant import months, constants
from validators import valid_year_month_in_database
from analytics import export_budget_csv

def open_budget_window(window:tk.Tk):
    '''Function to open the budget management window and operate on this window with different frames and widgets.
    args:
        window: the main window
    returns:
        None'''
    #   creating a new window for the budgets
    new_budget_window = tk.Toplevel(window)
    new_budget_window.title("Budget Management")
    new_budget_window.geometry("800x700")
    new_budget_window.grid_rowconfigure(0, weight=1)
    new_budget_window.grid_columnconfigure(1, weight=3)
    #creating a new frame for the side bar with butttons
    budget_frame = tk.Frame(new_budget_window, padx=10, pady=10, bg="#9c0b0b",relief="raised",bd=5)
    budget_frame.grid(row=0, column=0, sticky="nsew")
    budget_frame.grid_columnconfigure(0, weight=1)
    #creating a new main content frame for better layout management
    budget_content_frame = tk.Frame(new_budget_window, padx=10, pady=10, bg="#c01010")
    budget_content_frame.grid(row=0, column=1, sticky="nsew")
    budget_content_frame.grid_columnconfigure(0, weight=1)
    budget_content_frame.grid_rowconfigure (0, weight=1)
    #button for entering new budget
    new_budget_btn = tk.Button(budget_frame, text="Add New Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:new_budget_ui(budget_content_frame))
    new_budget_btn.grid(row=0, column=0, pady=(10,0))
    #button for deleting exisitng (calls GUI helper, not DB function)
    delete_budget_btn = tk.Button(budget_frame, text="Delete Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: delete_budget_ui(budget_content_frame))
    delete_budget_btn.grid(row=1, column=0, pady=(10,0))
    #button for updating existing budget
    update_budget_btn = tk.Button(budget_frame, text="Update Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: update_budget_ui(budget_content_frame))
    update_budget_btn.grid(row=2, column=0, pady=(10,0))
    #button for viewing budgets
    view_budgets_btn = tk.Button(budget_frame, text="View Budgets", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_budgets_ui(budget_content_frame))
    view_budgets_btn.grid(row=3, column=0, pady=(10,0))

    budget_destroy_btn = tk.Button(budget_frame, text="Close", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=new_budget_window.destroy)
    budget_destroy_btn.grid(row=6, column=0, pady=(10,0))

def new_budget_ui(budget_content_frame:tk.Frame):
    '''Function to add a new budget to the database by creating a new frame in the same window
          when called after clearing all three existing frames in the same window.
          It also resizes appropriately according to the window size
        args:
            budget_content_frame: The frame where the new budget frame will be created.
        returns:
            None'''
    #clear_content ensures that all the existing frames are cleared before entering new data
    clear_content(budget_content_frame)
    new_budget_frame = tk.Frame(budget_content_frame, padx=10, pady=10, bg="#c01010")
    new_budget_frame.grid(row=0, column=0, sticky="nsew")

    new_budget_frame.grid_columnconfigure(0, weight=1)
    
    new_budget_lbl = tk.Label(new_budget_frame, text="Add New Budget", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    new_budget_lbl.grid(row=0, column=0,pady=(10,0))

    new_budget_monthly_btn = tk.Button(new_budget_frame, text="Set Monthly Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:new_budget_monthly(new_budget_frame))
    new_budget_monthly_btn.grid(row=1, column=0, pady=(20,0))

    new_budget_category_btn = tk.Button(new_budget_frame, text="Set Monthly Category Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:new_budget_category(new_budget_frame))
    new_budget_category_btn.grid(row=2, column=0, pady=(20,0))

    new_budget_payment_method_btn = tk.Button(new_budget_frame, text="Set Monthly Payment Method Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:new_budget_payment_method(new_budget_frame))
    new_budget_payment_method_btn.grid(row=3, column=0, pady=(20,0))

def new_budget_monthly(new_budget_frame:tk.Frame):
    '''Function to add a new budget to the database by creating a new frame in the same window.
        It also resizes appropriately according to the window size
        it provides a combobox to select the month (in text)and a text entry to enter the budget limit.
    args:
        new_budget_frame: The frame where the new budget frame will be created.
    returns:
        None'''
    #clear_content ensures that all the existing frames are cleared before entering new data
    clear_content(new_budget_frame)
    new_budget_monthly_frame = tk.Frame(new_budget_frame, padx=10, pady=10, bg="#c01010")
    new_budget_monthly_frame.grid(row=0, column=0, sticky="nsew")
    new_budget_monthly_frame.grid_columnconfigure(0, weight=1)

    new_budget_monthly_lbl = tk.Label(new_budget_monthly_frame, text="Set Monthly Budget", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    new_budget_monthly_lbl.grid(row=0, column=0,pady=(10,0))

    new_budget_monthly_year_lbl = tk.Label(new_budget_monthly_frame, text="Year:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_monthly_year_lbl.grid(row=1, column=0, pady=(20,0))
    new_budget_monthly_year_entry = tk.Entry(new_budget_monthly_frame, width=4, font=("Arial", 16), justify="center")
    new_budget_monthly_year_entry.grid(row=2, column=0, pady=(10,0))

    new_budget_monthly_month_lbl = tk.Label(new_budget_monthly_frame, text="Month:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_monthly_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    new_budget_monthly_month_combobox = ttk.Combobox(new_budget_monthly_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    new_budget_monthly_month_combobox.grid(row=4, column=0, pady=(10,0))

    new_budget_monthly_budget_lbl = tk.Label(new_budget_monthly_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_monthly_budget_lbl.grid(row=5, column=0, pady=(20,0))
    new_budget_monthly_budget_entry = tk.Entry(new_budget_monthly_frame, width=20, font=("Arial", 16), justify="center")
    new_budget_monthly_budget_entry.grid(row=6, column=0, pady=(10,0))

    def submit_new_budget_monthly():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = new_budget_monthly_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == new_budget_monthly_month_combobox.get():
                break
        #validate the amount
        try:
            amount = float(new_budget_monthly_budget_entry.get())
        except ValueError as ve:
            messagebox.showerror("Error", str(ve)) 
            return

        valid,message = set_update_monthly_budget(year, month, amount)
        if valid:
            messagebox.showinfo("Success", message)
            new_budget_monthly_frame.destroy()
        else:
            messagebox.showerror("Error", message)

    new_budget_monthly_save_btn = tk.Button(new_budget_monthly_frame, text="Save Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=submit_new_budget_monthly)
    new_budget_monthly_save_btn.grid(row=7, column=0, pady=(20,0))

def new_budget_category(new_budget_frame:tk.Frame):
    '''Function to add a new budget to the database by creating a new frame in the same window.
        It also resizes appropriately according to the window size
        it provides a combobox to select the month (in text)and a text entry to enter the budget limit.
        it also provides a combobox to select the category and a text entry to enter the budget limit.
    args:
        new_budget_frame: The frame where the new budget frame will be created.
    returns:
        None'''
    #clear_content ensures that all the existing frames are cleared before entering new data
    clear_content(new_budget_frame)
    new_budget_category_frame = tk.Frame(new_budget_frame, padx=10, pady=10, bg="#c01010")
    new_budget_category_frame.grid(row=0, column=0, sticky="nsew")
    new_budget_category_frame.grid_columnconfigure(0, weight=1)

    new_budget_category_lbl = tk.Label(new_budget_category_frame, text="Set Monthly Category Budget", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    new_budget_category_lbl.grid(row=0, column=0,pady=(10,0))

    new_budget_category_year_lbl = tk.Label(new_budget_category_frame, text="Year:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_category_year_lbl.grid(row=1, column=0, pady=(20,0))
    new_budget_category_year_entry = tk.Entry(new_budget_category_frame, width=4, font=("Arial", 16), justify="center")
    new_budget_category_year_entry.grid(row=2, column=0, pady=(10,0))

    new_budget_category_month_lbl = tk.Label(new_budget_category_frame, text="Month:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_category_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    new_budget_category_month_combobox = ttk.Combobox(new_budget_category_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    new_budget_category_month_combobox.grid(row=4, column=0, pady=(10,0))

    new_budget_category_category_lbl = tk.Label(new_budget_category_frame, text="Category:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_category_category_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the category
    new_budget_category_category_combobox = ttk.Combobox(new_budget_category_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
    new_budget_category_category_combobox.grid(row=6, column=0, pady=(10,0))

    new_budget_category_budget_lbl = tk.Label(new_budget_category_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_category_budget_lbl.grid(row=7, column=0, pady=(20,0))
    new_budget_category_budget_entry = tk.Entry(new_budget_category_frame, width=20, font=("Arial", 16), justify="center")
    new_budget_category_budget_entry.grid(row=8, column=0, pady=(10,0))

    def submit_new_budget_category():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = new_budget_category_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == new_budget_category_month_combobox.get():
                break
        #validate the amount
        try:
            amount = float(new_budget_category_budget_entry.get())
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        category = new_budget_category_category_combobox.get()
        valid,message = set_update_monthly_category_budget(year, month, category, amount)
        if valid:
            messagebox.showinfo("Success", message)
            new_budget_category_frame.destroy()
        else:
            messagebox.showerror("Error", message)
    
    new_budget_category_save_btn = tk.Button(new_budget_category_frame, text="Save Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=submit_new_budget_category)
    new_budget_category_save_btn.grid(row=9, column=0, pady=(20,0))


def new_budget_payment_method(new_budget_frame:tk.Frame):
    '''Function to add a new budget to the database by creating a new frame in the same window.
        It also resizes appropriately according to the window size
        it provides a combobox to select the month (in text)and a text entry to enter the budget limit.
        it also provides a combobox to select the payment method and a text entry to enter the budget limit.
    args:
        new_budget_frame: The frame where the new budget frame will be created.
    returns:
        None'''
    #clear_content ensures that all the existing frames are cleared before entering new data
    clear_content(new_budget_frame)
    new_budget_payment_method_frame = tk.Frame(new_budget_frame, padx=10, pady=10, bg="#c01010")
    new_budget_payment_method_frame.grid(row=0, column=0, sticky="nsew")
    new_budget_payment_method_frame.grid_columnconfigure(0, weight=1)

    new_budget_payment_method_lbl = tk.Label(new_budget_payment_method_frame, text="Set Monthly Payment Method Budget", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    new_budget_payment_method_lbl.grid(row=0, column=0,pady=(10,0))

    new_budget_payment_method_year_lbl = tk.Label(new_budget_payment_method_frame, text="Year:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_payment_method_year_lbl.grid(row=1, column=0, pady=(20,0))
    new_budget_payment_method_year_entry = tk.Entry(new_budget_payment_method_frame, width=4, font=("Arial", 16), justify="center")
    new_budget_payment_method_year_entry.grid(row=2, column=0, pady=(10,0))

    new_budget_payment_method_month_lbl = tk.Label(new_budget_payment_method_frame, text="Month:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_payment_method_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    new_budget_payment_method_month_combobox = ttk.Combobox(new_budget_payment_method_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    new_budget_payment_method_month_combobox.grid(row=4, column=0, pady=(10,0))

    new_budget_payment_method_payment_method_lbl = tk.Label(new_budget_payment_method_frame, text="Payment Method:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_payment_method_payment_method_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the payment method
    new_budget_payment_method_payment_method_combobox = ttk.Combobox(new_budget_payment_method_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'],textvariable=tk.StringVar(), state="readonly",justify="center")
    new_budget_payment_method_payment_method_combobox.grid(row=6, column=0, pady=(10,0))
        
    new_budget_payment_method_budget_lbl = tk.Label(new_budget_payment_method_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    new_budget_payment_method_budget_lbl.grid(row=7, column=0, pady=(20,0))
    new_budget_payment_method_budget_entry = tk.Entry(new_budget_payment_method_frame, width=20, font=("Arial", 16), justify="center")

    def submit_new_budget_payment_method():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = new_budget_payment_method_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == new_budget_payment_method_month_combobox.get():
                break
        #validate the amount
        try:
            amount = float(new_budget_payment_method_budget_entry.get())
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        payment_method = new_budget_payment_method_payment_method_combobox.get()
        valid,message = set_update_monthly_payment_method_budget(year, month, payment_method, amount)
        if valid:
            messagebox.showinfo("Success", message)
            new_budget_payment_method_frame.destroy()
        else:
            messagebox.showerror("Error", message)
    
    new_budget_payment_method_save_btn = tk.Button(new_budget_payment_method_frame, text="Save Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=submit_new_budget_payment_method)
    new_budget_payment_method_save_btn.grid(row=9, column=0, pady=(20,0))

def delete_budget_ui(budget_content_frame:tk.Frame):
    '''Function to delete a budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    args:
        budget_content_frame: The frame where the delete budget frame will be created.
    returns:
        None'''
    clear_content(budget_content_frame)
    delete_budget_frame = tk.Frame(budget_content_frame, padx=10, pady=10, bg="#c01010")
    delete_budget_frame.grid(row=0, column=0, sticky="nsew")
    delete_budget_frame.grid_columnconfigure(0, weight=1)    
    delete_budget_lbl = tk.Label(delete_budget_frame, text="Delete Budget", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    delete_budget_lbl.grid(row=0, column=0,pady=(10,0))

    delete_budget_monthly_btn = tk.Button(delete_budget_frame, text="Delete Monthly Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: delete_budget_monthly_ui(delete_budget_frame))
    delete_budget_monthly_btn.grid(row=2, column=0, pady=(20,0))

    delete_budget_category_btn = tk.Button(delete_budget_frame, text="Delete Monthly Category Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: delete_budget_category_ui(delete_budget_frame))
    delete_budget_category_btn.grid(row=4, column=0, pady=(20,0))

    delete_budget_payment_method_btn = tk.Button(delete_budget_frame, text="Delete Monthly \nPayment Method Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: delete_budget_payment_method_ui(delete_budget_frame))
    delete_budget_payment_method_btn.grid(row=6, column=0, pady=(20,0))

def delete_budget_monthly_ui(delete_budget_frame:tk.Frame):
    '''Function to delete a monthly budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    args:
        delete_budget_frame: The frame where the delete monthly budget frame will be created.
    returns:
        None'''
    clear_content(delete_budget_frame)
    delete_budget_monthly_frame = tk.Frame(delete_budget_frame, padx=10, pady=10, bg="#c01010")
    delete_budget_monthly_frame.grid(row=0, column=0, sticky="nsew")
    delete_budget_monthly_frame.grid_columnconfigure(0, weight=1)    
    delete_budget_lbl = tk.Label(delete_budget_monthly_frame, text="Delete Monthly Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    delete_budget_lbl.grid(row=0, column=0,pady=(10,0))
    delete_budget_monthly_year_lbl = tk.Label(delete_budget_monthly_frame, text="Year:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_monthly_year_lbl.grid(row=1, column=0, pady=(20,0))
    delete_budget_monthly_year_entry = tk.Entry(delete_budget_monthly_frame, width=4, font=("Arial", 16), justify="center")
    delete_budget_monthly_year_entry.grid(row=2, column=0, pady=(10,0))

    delete_budget_monthly_month_lbl = tk.Label(delete_budget_monthly_frame, text="Month:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_monthly_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    delete_budget_monthly_month_combobox = ttk.Combobox(delete_budget_monthly_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    delete_budget_monthly_month_combobox.grid(row=4, column=0, pady=(10,0))

    def submit_delete_budget_monthly():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = delete_budget_monthly_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == delete_budget_monthly_month_combobox.get():
                break
        valid,message = delete_budget_limit(year, month)
        if valid:
            messagebox.showinfo("Success", message)
            delete_budget_monthly_frame.destroy()
        else:
            messagebox.showerror("Error", message)

    delete_budget_monthly_save_btn = tk.Button(delete_budget_monthly_frame, text="Delete Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=submit_delete_budget_monthly)
    delete_budget_monthly_save_btn.grid(row=5, column=0, pady=(20,0))

def delete_budget_category_ui(delete_budget_frame:tk.Frame):
    '''Function to delete a monthly category budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    args:
        delete_budget_frame: The frame where the delete monthly category budget frame will be created.
    returns:
        None'''
    clear_content(delete_budget_frame)
    delete_budget_category_frame = tk.Frame(delete_budget_frame, padx=10, pady=10, bg="#c01010")
    delete_budget_category_frame.grid(row=0, column=0, sticky="nsew")
    delete_budget_category_frame.grid_columnconfigure(0, weight=1)    
    delete_budget_lbl = tk.Label(delete_budget_category_frame, text="Delete Monthly\nCategory Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    delete_budget_lbl.grid(row=0, column=0,pady=(10,0))
    delete_budget_category_year_lbl = tk.Label(delete_budget_category_frame, text="Year:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_category_year_lbl.grid(row=1, column=0, pady=(20,0))
    delete_budget_category_year_entry = tk.Entry(delete_budget_category_frame, width=4, font=("Arial", 16), justify="center")
    delete_budget_category_year_entry.grid(row=2, column=0, pady=(10,0))

    delete_budget_category_month_lbl = tk.Label(delete_budget_category_frame, text="Month:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_category_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    delete_budget_category_month_combobox = ttk.Combobox(delete_budget_category_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    delete_budget_category_month_combobox.grid(row=4, column=0, pady=(10,0))

    delete_budget_category_category_lbl = tk.Label(delete_budget_category_frame, text="Category:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_category_category_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the category
    delete_budget_category_category_combobox = ttk.Combobox(delete_budget_category_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
    delete_budget_category_category_combobox.grid(row=6, column=0, pady=(10,0))

    def submit_delete_budget_category():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = delete_budget_category_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == delete_budget_category_month_combobox.get():
                break
        category = delete_budget_category_category_combobox.get()
        if category == "":
            tk.messagebox.showerror("Error", "Category cannot be empty.")            
            return
        valid,message = delete_budget_limit(year, month, category)
        if valid:
            messagebox.showinfo("Success", message)
            delete_budget_category_frame.destroy()
        else:
            messagebox.showerror("Error", message)

    delete_budget_category_save_btn = tk.Button(delete_budget_category_frame, text="Delete Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=submit_delete_budget_category)
    delete_budget_category_save_btn.grid(row=7, column=0, pady=(20,0))

def delete_budget_payment_method_ui(delete_budget_frame:tk.Frame):
    '''Function to delete a monthly payment method budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    args:
        delete_budget_frame: The frame where the delete monthly payment method budget frame will be created.
    returns:
        None'''
    clear_content(delete_budget_frame)
    delete_budget_payment_method_frame = tk.Frame(delete_budget_frame, padx=10, pady=10, bg="#c01010")
    delete_budget_payment_method_frame.grid(row=0, column=0, sticky="nsew")
    delete_budget_payment_method_frame.grid_columnconfigure(0, weight=1)    
    delete_budget_lbl = tk.Label(delete_budget_payment_method_frame, text="Delete Monthly \nPayment Method Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    delete_budget_lbl.grid(row=0, column=0,pady=(10,0))
    delete_budget_payment_method_year_lbl = tk.Label(delete_budget_payment_method_frame, text="Year:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_payment_method_year_lbl.grid(row=1, column=0, pady=(20,0))
    delete_budget_payment_method_year_entry = tk.Entry(delete_budget_payment_method_frame, width=4, font=("Arial", 16), justify="center")
    delete_budget_payment_method_year_entry.grid(row=2, column=0, pady=(10,0))

    delete_budget_payment_method_month_lbl = tk.Label(delete_budget_payment_method_frame, text="Month:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_payment_method_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    delete_budget_payment_method_month_combobox = ttk.Combobox(delete_budget_payment_method_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    delete_budget_payment_method_month_combobox.grid(row=4, column=0, pady=(10,0))

    delete_budget_payment_method_payment_method_lbl = tk.Label(delete_budget_payment_method_frame, text="Payment Method:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    delete_budget_payment_method_payment_method_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the payment method
    delete_budget_payment_method_payment_method_combobox = ttk.Combobox(delete_budget_payment_method_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'],textvariable=tk.StringVar(), state="readonly",justify="center")
    delete_budget_payment_method_payment_method_combobox.grid(row=6, column=0, pady=(10,0))
    def submit_delete_budget_payment_method():
        '''Function to submit the new budget to the database when called.
        args:
            None
        returns:
            None'''
        year = delete_budget_payment_method_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == delete_budget_payment_method_month_combobox.get():
                break
        payment_method = delete_budget_payment_method_payment_method_combobox.get()
        if payment_method == "":
            tk.messagebox.showerror("Error", "Payment method cannot be empty.")
            return
        valid,message = delete_budget_limit(year, month, payment_method)
        if valid:
            messagebox.showinfo("Success", message)
            delete_budget_payment_method_frame.destroy()
        else:
            messagebox.showerror("Error", message)

    delete_budget_payment_method_save_btn = tk.Button(delete_budget_payment_method_frame, text="Delete Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=submit_delete_budget_payment_method)
    delete_budget_payment_method_save_btn.grid(row=7, column=0, pady=(20,0))

def update_budget_ui(budget_content_frame:tk.Frame):
    '''Function to update an existing budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.it also resizes appropriately according to the window size
    args:
        budget_content_frame: The frame where the update budget frame will be created.
    returns:
        None'''
    #clear existing frames before opening the update budget frame
    clear_content(budget_content_frame)
    update_budget_frame = tk.Frame(budget_content_frame, padx=10, pady=10, bg="#c01010")
    update_budget_frame.grid(row=0, column=0, sticky="nsew")
    update_budget_frame.grid_columnconfigure(0, weight=1)
    update_budget_lbl = tk.Label(update_budget_frame, text="Update Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    update_budget_lbl.grid(row=0, column=0,pady=(10,0))

    update_budget_monthly_btn = tk.Button(update_budget_frame, text="Update Monthly Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:update_budget_monthly(update_budget_frame))
    update_budget_monthly_btn.grid(row=2, column=0, pady=(20,0))

    update_budget_category_btn = tk.Button(update_budget_frame, text="Update Monthly Category Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:update_budget_category(update_budget_frame))
    update_budget_category_btn.grid(row=3, column=0, pady=(20,0))

    update_budget_payment_method_btn = tk.Button(update_budget_frame, text="Update Monthly Payment Method Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command= lambda:update_budget_payment_method(update_budget_frame))
    update_budget_payment_method_btn.grid(row=4, column=0, pady=(20,0))

def update_budget_monthly(update_budget_frame:tk.Frame):
    '''Function to update an existing budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.it also resizes appropriately according to the window size
    args:
        update_budget_frame: The frame where the update budget frame will be created.
    returns:
        None'''
    #clear existing frames before opening the update budget frame
    clear_content(update_budget_frame)
    update_budget_monthly_frame = tk.Frame(update_budget_frame, padx=10, pady=10, bg="#c01010")
    update_budget_monthly_frame.grid(row=0, column=0, sticky="nsew")
    update_budget_monthly_frame.grid_columnconfigure(0, weight=1)
    update_budget_monthly_lbl = tk.Label(update_budget_monthly_frame, text="Update Monthly Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    update_budget_monthly_lbl.grid(row=0, column=0,pady=(10,0))

    update_budget_monthly_year_lbl = tk.Label(update_budget_monthly_frame, text="Year:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_monthly_year_lbl.grid(row=1, column=0, pady=(20,0))
    update_budget_monthly_year_entry = tk.Entry(update_budget_monthly_frame, width=4, font=("Arial", 16), justify="center")
    update_budget_monthly_year_entry.grid(row=2, column=0, pady=(6,0))

    update_budget_monthly_month_lbl = tk.Label(update_budget_monthly_frame, text="Month:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_monthly_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    update_budget_monthly_month_combobox = ttk.Combobox(update_budget_monthly_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    update_budget_monthly_month_combobox.grid(row=4, column=0, pady=(10,0))

    update_budget_monthly_budget_lbl = tk.Label(update_budget_monthly_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_monthly_budget_lbl.grid(row=5, column=0, pady=(20,0))
    update_budget_monthly_budget_entry = tk.Entry(update_budget_monthly_frame, width=20, font=("Arial", 16), justify="center")
    update_budget_monthly_budget_entry.grid(row=6, column=0, pady=(6,0))    

    def submit_update_budget_monthly():
        '''Function to submit the updated budget to the database when called.
        args:
            None
        returns:
            None'''
        year = update_budget_monthly_year_entry.get()
        try:
            year = int(year)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        # the months corresponding number is fed as month
        for month, value in months.items():
            if value == update_budget_monthly_month_combobox.get():
                break
        if not valid_year_month_in_database(year, month,"budget.db","monthly_budget"):
            tk.messagebox.showerror("Error", "Invalid year and month. Please enter a valid year and month.")
            return
        
        #validate the amount
        try:
            amount = float(update_budget_monthly_budget_entry.get())
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        valid,message = set_update_monthly_budget(year, month, amount)
        if valid:
            messagebox.showinfo("Success", message)
            update_budget_monthly_frame.destroy()
        else:
            messagebox.showerror("Error", message)  

    update_budget_monthly_save_btn = tk.Button(update_budget_monthly_frame, text="Update Budget", font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd=6, relief="raised", justify="center", command=submit_update_budget_monthly)
    update_budget_monthly_save_btn.grid(row=7, column=0, pady=(10,0))

def update_budget_category(update_budget_frame:tk.Frame):
    '''Function to update an existing budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.it also resizes appropriately according to the window size
    args:
        update_budget_frame: The frame where the update budget frame will be created.
    returns:
        None'''
    #clear existing frames before opening the update budget frame
    clear_content(update_budget_frame)
    update_budget_category_frame = tk.Frame(update_budget_frame, padx=10, pady=10, bg="#c01010")
    update_budget_category_frame.grid(row=0, column=0, sticky="nsew")
    update_budget_category_frame.grid_columnconfigure(0, weight=1)
    update_budget_category_lbl = tk.Label(update_budget_category_frame, text="Update Monthly \nCategory Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    update_budget_category_lbl.grid(row=0, column=0,pady=(10,0))

    update_budget_category_year_lbl = tk.Label(update_budget_category_frame, text="Year:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_category_year_lbl.grid(row=1, column=0, pady=(20,0))
    update_budget_category_year_entry = tk.Entry(update_budget_category_frame, width=4, font=("Arial", 16), justify="center")
    update_budget_category_year_entry.grid(row=2, column=0, pady=(6,0))

    update_budget_category_month_lbl = tk.Label(update_budget_category_frame, text="Month:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_category_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    update_budget_category_month_combobox = ttk.Combobox(update_budget_category_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")
    update_budget_category_month_combobox.grid(row=4, column=0, pady=(10,0))

    update_budget_category_category_lbl = tk.Label(update_budget_category_frame, text="Category:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_category_category_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the category
    update_budget_category_category_combobox = ttk.Combobox(update_budget_category_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
    update_budget_category_category_combobox.grid(row=6, column=0, pady=(10,0))

    update_budget_category_budget_lbl = tk.Label(update_budget_category_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_category_budget_lbl.grid(row=7, column=0, pady=(20,0))
    update_budget_category_budget_entry = tk.Entry(update_budget_category_frame, width=20, font=("Arial", 16), justify="center")
    update_budget_category_budget_entry.grid(row=8, column=0, pady=(6,0))

    def submit_update_budget_category():
        '''Function to submit the updated budget to the database when called.
        args:
            None
        returns:
            None'''
        year = update_budget_category_year_entry.get()
        try:
            year = int(year)    
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        for month, value in months.items():
            if value == update_budget_category_month_combobox.get():
                break
        if not valid_year_month_in_database(year, month,"budget.db","monthly_category_budget"):
            tk.messagebox.showerror("Error", "Invalid year and month. Please enter a valid year and month.")
            return
        try:
            amount = float(update_budget_category_budget_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid amount. Please enter a valid amount.")
            return
        category = update_budget_category_category_combobox.get()
        if category == "":
            tk.messagebox.showerror("Error", "Category cannot be empty.")
            return
        valid,message = set_update_monthly_category_budget(year, month, category, amount)
        if valid:
            tk.messagebox.showinfo("Success", message)
            update_budget_category_frame.destroy()
        else:    
            tk.messagebox.showerror("Error", message)   
    update_budget_category_save_btn = tk.Button(update_budget_category_frame, text="Update Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=submit_update_budget_category)
    update_budget_category_save_btn.grid(row=9, column=0, pady=(10,0))

def update_budget_payment_method(update_budget_frame:tk.Frame):
    '''Function to update an existing budget from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.it also resizes appropriately according to the window size
    args:
        update_budget_frame: The frame where the update budget frame will be created.
    returns:
        None'''
    #clear existing frames before opening the update budget frame
    clear_content(update_budget_frame)
    update_budget_payment_method_frame = tk.Frame(update_budget_frame, padx=10, pady=10, bg="#c01010")
    update_budget_payment_method_frame.grid(row=0, column=0, sticky="nsew")
    update_budget_payment_method_frame.grid_columnconfigure(0, weight=1)
    update_budget_payment_method_lbl = tk.Label(update_budget_payment_method_frame, text="Update Monthly \nPayment Method Budget", font=("Arial", 30, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    update_budget_payment_method_lbl.grid(row=0, column=0,pady=(10,0))

    update_budget_payment_method_year_lbl = tk.Label(update_budget_payment_method_frame, text="Year:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_payment_method_year_lbl.grid(row=1, column=0, pady=(20,0))
    update_budget_payment_method_year_entry = tk.Entry(update_budget_payment_method_frame, width=4, font=("Arial", 16), justify="center")
    update_budget_payment_method_year_entry.grid(row=2, column=0, pady=(6,0))   

    update_budget_payment_method_month_lbl = tk.Label(update_budget_payment_method_frame, text="Month:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_payment_method_month_lbl.grid(row=3, column=0, pady=(20,0))
    # create a combobox to select the month as jan to dec
    update_budget_payment_method_month_combobox = ttk.Combobox(update_budget_payment_method_frame, width=4, font=("Arial", 16), values=list(months.values()),textvariable=tk.StringVar(), state="readonly",justify="center")    
    update_budget_payment_method_month_combobox.grid(row=4, column=0, pady=(10,0))

    update_budget_payment_method_payment_method_lbl = tk.Label(update_budget_payment_method_frame, text="Payment Method:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_payment_method_payment_method_lbl.grid(row=5, column=0, pady=(20,0))
    # create a combobox to select the payment method
    update_budget_payment_method_payment_method_combobox = ttk.Combobox(update_budget_payment_method_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'], textvariable=tk.StringVar(), state="readonly", justify="center")
    update_budget_payment_method_payment_method_combobox.grid(row=6, column=0, pady=(10,0))

    update_budget_payment_method_budget_lbl = tk.Label(update_budget_payment_method_frame, text="Budget Limit:", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
    update_budget_payment_method_budget_lbl.grid(row=7, column=0, pady=(20,0))
    update_budget_payment_method_budget_entry = tk.Entry(update_budget_payment_method_frame, width=20, font=("Arial", 16), justify="center")
    update_budget_payment_method_budget_entry.grid(row=8, column=0, pady=(6,0))

    def submit_update_budget_payment_method():
        '''Function to submit the updated budget to the database when called.
        args:
            None
        returns:
            None'''
        year = update_budget_payment_method_year_entry.get()
        try:
            year = int(year)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        for month, value in months.items():
            if value == update_budget_payment_method_month_combobox.get():
                break
        if not valid_year_month_in_database(year, month,"budget.db","monthly_payment_method_budget"):
            tk.messagebox.showerror("Error", "Invalid year and month. Please enter a valid year and month.")
            return
        try:
            amount = float(update_budget_payment_method_budget_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid amount. Please enter a valid amount.")
            return
        payment_method = update_budget_payment_method_payment_method_combobox.get()
        if payment_method == "":
            tk.messagebox.showerror("Error", "Payment method cannot be empty.")
            return
        valid,message = set_update_monthly_payment_method_budget(year, month, payment_method, amount)
        if valid:
            tk.messagebox.showinfo("Success", message)
            update_budget_payment_method_frame.destroy()
        else:    
            tk.messagebox.showerror("Error", message)   
    update_budget_payment_method_save_btn = tk.Button(update_budget_payment_method_frame, text="Update Budget", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=submit_update_budget_payment_method)
    update_budget_payment_method_save_btn.grid(row=9, column=0, pady=(10,0))

def view_budgets_ui(budget_content_frame:tk.Frame):
    '''creates a new frame for viewing the budgets from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    calls three seperate functions to fetch the budgets from the database and display them in the treeview, through buttons
    args:
        view_budgets_frame: The frame where the view budgets frame will be created.
    returns:
        None'''
    #clear existing frames before opening the view budgets frame
    clear_content(budget_content_frame)
    view_budgets_frame = tk.Frame(budget_content_frame, padx=10, pady=10, bg="#c01010")
    view_budgets_frame.grid(row=0, column=0, sticky="nsew")
    view_budgets_frame.grid_columnconfigure(0, weight=1)
    view_budgets_lbl = tk.Label(view_budgets_frame, text="View Budgets", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    view_budgets_lbl.grid(row=0, column=0,pady=(10,0))
    
    view_budgets_monthly_btn = tk.Button(view_budgets_frame, text="View Monthly Budgets", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_budgets_monthly_ui(view_budgets_frame,"budgets_monthly.csv"))
    view_budgets_monthly_btn.grid(row=1, column=0, pady=(20,0))

    view_budgets_category_btn = tk.Button(view_budgets_frame, text="View Monthly Category Budgets", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_budgets_category_ui(view_budgets_frame,"budgets_category.csv"))
    view_budgets_category_btn.grid(row=2, column=0, pady=(20,0))

    view_budgets_payment_method_btn = tk.Button(view_budgets_frame, text="View Monthly \nPayment Method Budgets", font=("Arial", 20, "bold"), bg="#1aab0a", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_budgets_payment_method_ui(view_budgets_frame,"budgets_payment_method.csv"))
    view_budgets_payment_method_btn.grid(row=3, column=0, pady=(20,0))

def view_budgets_monthly_ui(view_budgets_frame:tk.Frame,file_name:str):
    '''displays the monthly budgets from the database in a treeview
    the column headers are id,year, month, amount_limit.
    the data is in the form of list of tuples where each tuple is a record
    displays each record in a seperate line under the respective header columns
    The frame contains both horizontal and vertical scrollbars and resizes appropriately according to the window size
    It also provides a button to export the budgets to a csv file,and returns a message box if the operation is successful or not.
    args:
        view_budgets_frame: The frame where the view budgets frame will be created.
        file_name: the name of the file to export the budgets to.
    returns:
        None'''
    clear_content(view_budgets_frame)
    view_budgets_monthly_frame = tk.Frame(view_budgets_frame, padx=10, pady=10, bg="#c01010")
    view_budgets_monthly_frame.grid(row=0, column=0, sticky="nsew")
    # Create a Treeview widget to display the expenses
    columns = ("id","year", "month", "amount_limit")
    tree = ttk.Treeview(view_budgets_monthly_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    # Fetch expenses from the database
    valid,budgets = get_all_budgets()
    if valid:
        for budget in budgets:
            tree.insert("", tk.END, values=budget)
    else:
        tk.messagebox.showerror("Error", "Failed to retrieve budgets.")
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(view_budgets_monthly_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky="ns")
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(view_budgets_monthly_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.grid(row=1, column=0, sticky="ew")
    # Place the Treeview widget
    tree.grid(row=0, column=0, sticky="nsew")
    view_budgets_monthly_frame.grid_rowconfigure(0, weight=1)
    view_budgets_monthly_frame.grid_columnconfigure(0, weight=1)

    export_budgets_btn = tk.Button(view_budgets_monthly_frame, text="Export Budgets", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=lambda: export_budget_csv_ui())
    export_budgets_btn.grid(row=2, column=0, pady=(20,0))

    def export_budget_csv_ui():
        '''Function to export budgets from the database by creating a new frame in the same window when called.
        also checks if the write operation is successful or not.And returns a message box if the operation is successful or not.
        args:
            None
        returns:
            None'''
        col_names = ["id","year", "month", "amount_limit"]
        file_path = save_file_dialogue(file_name)
        if not file_path:
            return
        valid = export_budget_csv(file_path,get_all_budgets(),col_names)
        if valid:
            messagebox.showinfo("Success", "Budgets exported successfully.")
            view_budgets_monthly_frame.destroy()
        else:
            messagebox.showerror("Error", "Failed to export budgets.")
            view_budgets_monthly_frame.destroy()

def view_budgets_category_ui(view_budgets_frame:tk.Frame,file_name:str):
    '''displays the monthly category budgets from the database in a treeview
    the column headers are id,year, month, category, amount_limit.
    the data is in the form of list of tuples where each tuple is a record
    displays each record in a seperate line under the respective header columns
    The frame contains both horizontal and vertical scrollbars and resizes appropriately according to the window size
    It also provides a button to export the budgets to a csv file,and returns a message box if the operation is successful or not.
    args:
        view_budgets_frame: The frame where the view budgets frame will be created.
        file_name: the name of the file to export the budgets to.
    returns:
        None'''
    clear_content(view_budgets_frame)
    view_budgets_category_frame = tk.Frame(view_budgets_frame, padx=10, pady=10, bg="#c01010")
    view_budgets_category_frame.grid(row=0, column=0, sticky="nsew")
    # Create a Treeview widget to display the expenses
    columns = ("id","year", "month", "category", "amount_limit")
    tree = ttk.Treeview(view_budgets_category_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    # Fetch expenses from the database
    valid,budgets = get_all_category_budgets()
    if valid:
        for budget in budgets:
            tree.insert("", tk.END, values=budget)
    else:
        tk.messagebox.showerror("Error", "Failed to retrieve budgets.")
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(view_budgets_category_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky="ns")
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(view_budgets_category_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.grid(row=1, column=0, sticky="ew")
    # Place the Treeview widget
    tree.grid(row=0, column=0, sticky="nsew")
    view_budgets_category_frame.grid_rowconfigure(0, weight=1)
    view_budgets_category_frame.grid_columnconfigure(0, weight=1)
    #create a button to export the budgets to a csv file
    export_budgets_btn = tk.Button(view_budgets_category_frame, text="Export Budgets", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=lambda: export_budget_csv_ui())
    export_budgets_btn.grid(row=2, column=0, pady=(20,0))
    def export_budget_csv_ui():
        '''Function to export budgets from the database by creating a new frame in the same window when called.
        also checks if the write operation is successful or not.And returns a message box if the operation is successful or not.
        args:
            None
        returns:
            None'''
        col_names = ["id","year", "month", "category", "amount_limit"]
        # opens a file dialogue to allow the user to decide the file path and file name, with a default file name as the one provided in the function argument.
        file_path = save_file_dialogue(file_name)
        if not file_path:
            return
        valid = export_budget_csv(file_path,get_all_category_budgets(),col_names)
        if valid:
            messagebox.showinfo("Success", "Budgets exported successfully.")
            view_budgets_category_frame.destroy()
        else:
            messagebox.showerror("Error", "Failed to export budgets.")
            view_budgets_category_frame.destroy()

def view_budgets_payment_method_ui(view_budgets_frame:tk.Frame,file_name:str):
    '''displays the monthly payment method budgets from the database in a treeview
    the column headers are id,year, month, payment_method, amount_limit.
    the data is in the form of list of tuples where each tuple is a record
    displays each record in a seperate line under the respective header columns
    The frame contains both horizontal and vertical scrollbars and resizes appropriately according to the window size
    args:
        view_budgets_frame: The frame where the view budgets frame will be created.
        file_name: the name of the file to export the budgets to.
    returns:
        None'''
    #clear existing frames before opening the view budgets frame
    clear_content(view_budgets_frame)
    view_budgets_payment_method_frame = tk.Frame(view_budgets_frame, padx=10, pady=10, bg="#c01010")
    view_budgets_payment_method_frame.grid(row=0, column=0, sticky="nsew")
    # Create a Treeview widget to display the expenses
    columns = ("id","year", "month", "payment_method", "amount_limit")
    tree = ttk.Treeview(view_budgets_payment_method_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    # Fetch expenses from the database
    valid,payment_method_budgets = get_all_payment_method_budgets()
    if valid:
        for payment_method_budget in payment_method_budgets:
            tree.insert("", tk.END, values=payment_method_budget)
    else:
        tk.messagebox.showerror("Error", "Failed to retrieve budgets.")
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(view_budgets_payment_method_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky="ns")
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(view_budgets_payment_method_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.grid(row=1, column=0, sticky="ew")
    # Place the Treeview widget
    tree.grid(row=0, column=0, sticky="nsew")
    view_budgets_payment_method_frame.grid_rowconfigure(0, weight=1)        
    view_budgets_payment_method_frame.grid_columnconfigure(0, weight=1)
    #create a button to export the budgets to a csv file
    export_budgets_btn = tk.Button(view_budgets_payment_method_frame, text="Export Budgets", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=lambda: export_budget_csv_ui())
    export_budgets_btn.grid(row=2, column=0, pady=(20,0))
    def export_budget_csv_ui():
        '''Function to export budgets from the database by creating a new frame in the same window when called.
        also checks if the write operation is successful or not.And returns a message box if the operation is successful or not.
        args:
            None
        returns:
            None'''
        # opens a file dialogue to allow the user to decide the file path and file name, with a default file name as the one provided in the function argument.
    
        col_names = ["id","year", "month", "payment_method", "amount_limit"]
        file_path = save_file_dialogue(file_name)
        if not file_path:
            return
        valid = export_budget_csv(file_path,get_all_payment_method_budgets(),col_names)
        if valid:
            messagebox.showinfo("Success", "Budgets exported successfully.")
            view_budgets_payment_method_frame.destroy()
        else:
            messagebox.showerror("Error", "Failed to export budgets.")            
            view_budgets_payment_method_frame.destroy()

