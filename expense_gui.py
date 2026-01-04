import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog
from tkcalendar import  DateEntry
from constant import constants
from expense import add_expense, delete_expense , update_expense,view_expenses, search_expenses, get_expense_by_id
from analytics import export_budget_csv, export_expense_csv

def open_expense_window(window:tk.Tk):
    '''Function to open the expense management window and operate on this window with different frames and widgets.
    args:
        window: the main window
    returns:
        None'''
#   creating a new window for the expenses
    new_expense_window = tk.Toplevel(window)
    new_expense_window.title("Expense Management")
    new_expense_window.geometry("800x700")
    new_expense_window.grid_rowconfigure(0, weight=1)
    new_expense_window.grid_columnconfigure(1, weight=3)
    #creating a new frame for the side bar with butttons
    expense_frame = tk.Frame(new_expense_window, padx=10, pady=10, bg="#9c0b0b",relief="raised",bd=5)
    expense_frame.grid(row=0, column=0, sticky="nsew")
    expense_frame.grid_columnconfigure(0, weight=1)
    #creating a new main content frame for better layout management
    expense_content_frame = tk.Frame(new_expense_window, padx=10, pady=10, bg="#c01010")
    expense_content_frame.grid(row=0, column=1, sticky="nsew")
    expense_content_frame.grid_columnconfigure(0, weight=1)
    expense_content_frame.grid_rowconfigure(0, weight=1)

    #button for entering new expense
    new_expense_btn = tk.Button(expense_frame, text="Add New Expense", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command= lambda:new_expense(expense_content_frame))
    new_expense_btn.grid(row=0, column=0, pady=(10,0))
    #button for deleting exisitng (calls GUI helper, not DB function)
    delete_expense_btn = tk.Button(expense_frame, text="Delete Expense", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=lambda: delete_expense_ui(expense_content_frame))
    delete_expense_btn.grid(row=1, column=0, pady=(10,0))
    #button for updating existing expense
    update_expense_btn = tk.Button(expense_frame, text="Update Expense", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: update_expense_ui(expense_content_frame))
    update_expense_btn.grid(row=2, column=0, pady=(10,0))
    #button for viewing expenses
    view_expenses_btn = tk.Button(expense_frame, text="View Expenses", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_expenses_ui(view_expenses(), expense_content_frame,file_name="expenses.csv"))
    view_expenses_btn.grid(row=3, column=0, pady=(10,0))

    search_expenses_btn = tk.Button(expense_frame, text="Search Expenses", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command= lambda: search_expenses_ui(expense_content_frame))
    search_expenses_btn.grid(row=4, column=0, pady=(10,0))


    expense_destroy_btn = tk.Button(expense_frame, text="Close", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=new_expense_window.destroy)
    expense_destroy_btn.grid(row=5, column=0, pady=(10,0))

def clear_content(expense_content_frame:tk.Frame):
    '''Clears all content from the main frame, before opening a new frame
    args:
         expense_content_frame : the main content frame to clear
    returns:
    None'''
    for widget in expense_content_frame.winfo_children():
        widget.destroy()
def new_expense(expense_content_frame:tk.Frame):
        '''Function to add a new expense to the database by creating a new frame in the same window
          when called after clearing all three existing frames in the same window.
          it also has a vertical scroll feature fitting the exact length
        of the frame to accommodate all options
        it also resizes approprialtely according to the window size
        args:
            expense_content_frame: The frame where the new expense frame will be created.
        returns:
            None'''
        #clear_content ensures that all the existing frames are cleared before entering new data
        clear_content(expense_content_frame)
        #creating vertical scroll
        new_expense_canvas = tk.Canvas(expense_content_frame, bg="#c01010")
        new_expense_canvas.grid(row=0, column=0, sticky="nsew")

        new_expense_scrollbar = tk.Scrollbar(expense_content_frame, orient="vertical", command=new_expense_canvas.yview)
        new_expense_scrollbar.grid(row=0, column=1, sticky="ns")
        new_expense_frame = tk.Frame(new_expense_canvas, bg="#c01010", padx=10, pady=10)
        new_expense_canvas.configure(yscrollcommand=new_expense_scrollbar.set)
        new_expense_canvas.create_window((0, 0), window=new_expense_frame, anchor="nw")
        def on_configure(event):
            new_expense_canvas.configure(scrollregion=new_expense_canvas.bbox("all"))
            new_expense_canvas.itemconfig("all", width=event.width)
        new_expense_canvas.bind("<Configure>", on_configure)
        new_expense_frame.grid_columnconfigure(0, weight=1)
    
        new_expense_lbl = tk.Label(new_expense_frame, text="Add New Expense", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd=5, relief="ridge", justify="center")
        new_expense_lbl.grid(row=0, column=0, pady=(10, 0))

        new_date_lbl = tk.Label(new_expense_frame, text="Date:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_date_lbl.grid(row=1, column=0, pady=(20,0))
        new_date_entry = DateEntry(new_expense_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 16), date_pattern='yyyy-mm-dd',justify="center")
        new_date_entry.grid(row=2, column=0, pady=(10,0))

        new_amount_lbl = tk.Label(new_expense_frame, text="Amount:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_amount_lbl.grid(row=3, column=0, pady=(20,0))
        new_amount_entry = tk.Entry(new_expense_frame, width=20, font=("Arial", 16),justify="center")
        new_amount_entry.grid(row=4, column=0, pady=(10,0))

        new_category_lbl = tk.Label(new_expense_frame, text="Category:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_category_lbl.grid(row=5, column=0, pady=(20,0))
        #combobox allows user to select from predefined categories
        new_category_combobox = ttk.Combobox(new_expense_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
        new_category_combobox.grid(row=6, column=0, pady=(10,0))

        new_description_lbl = tk.Label(new_expense_frame, text="Description:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_description_lbl.grid(row=7, column=0, pady=(20,0))
        new_description_entry = tk.Entry(new_expense_frame, width=20, font=("Arial", 16),justify="center")
        new_description_entry.grid(row=8, column=0, pady=(10,0))

        new_payment_method_lbl = tk.Label(new_expense_frame, text="Payment Method:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_payment_method_lbl.grid(row=9, column=0, pady=(20,0))
        #combobox allows user to select from predefined payment methods
        new_payment_method_combobox = ttk.Combobox(new_expense_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'],textvariable=tk.StringVar(), state="readonly",justify="center")
        new_payment_method_combobox.grid(row=10, column=0, pady=(10,0))

        # check button asks the user if exceeding the budget is fine while entering the expense
        new_expense_var = tk.BooleanVar(value=False)
        new_expense_check_btn = tk.Checkbutton(new_expense_frame, text=" Exceeding budget is fine", font=("Arial", 16), bg="#c01010", fg="black", justify="center", variable=new_expense_var, onvalue=True, offvalue=False)
        new_expense_check_btn.grid(row=11, column=0, pady=(10,0))

        def submit_new_expense():
            '''Function to submit the new expense to the database when called.
            args:
                None
            returns:
                None'''
            date = new_date_entry.get()
            try:
                amount = float(new_amount_entry.get())
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                return
            category = new_category_combobox.get()
            description = new_description_entry.get()
            payment_method = new_payment_method_combobox.get()
            exceed_budget= new_expense_var.get()
            valid,message = add_expense(date, amount, category, description, payment_method, exceed_budget)
            if valid:
                messagebox.showinfo("Success", message)
                new_expense_frame.destroy()
            else:
                messagebox.showerror("Error", message)
            
                                     
        new_expense_save_btn = tk.Button(new_expense_frame, text="Save Expense", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=submit_new_expense)
        new_expense_save_btn.grid(row=12, column=0, pady=(20,0))


def delete_expense_ui(expense_content_frame:tk.Frame):
    '''Function to delete an expense from the database by creating a new frame in the same window when called, 
    after clearing all the existing frames.
    args:
        expense_content_frame: The frame where the delete expense frame will be created.
    returns:
        None'''
    clear_content(expense_content_frame)
    delete_expense_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    delete_expense_frame.grid(row=0, column=0, sticky="nsew")
    delete_expense_frame.grid_columnconfigure(0, weight=1)    
    delete_expense_lbl = tk.Label(delete_expense_frame, text="Delete Expense", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    delete_expense_lbl.grid(row=0, column=0,pady=(10,0))

    delete_expense_id_lbl = tk.Label(delete_expense_frame, text="Expense ID:", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd = 3, relief="solid", justify="center")
    delete_expense_id_lbl.grid(row=1, column=0, pady=(20,0))
    delete_expense_id_entry = tk.Entry(delete_expense_frame, width=20, font=("Arial", 16),justify="center")
    delete_expense_id_entry.grid(row=2, column=0, pady=(10,0))

    def delete_expense_id():
        try:
            expense_id = int(delete_expense_id_entry.get())
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        valid,message = delete_expense(expense_id)
        if valid:
            messagebox.showinfo("Success", message)
            delete_expense_frame.destroy()
        else:
            messagebox.showerror("Error", message)

    delete_expense_id_btn = tk.Button(delete_expense_frame, text="Delete Expense", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=delete_expense_id)
    delete_expense_id_btn.grid(row=3, column=0, pady=(20,0))

def update_expense_ui(expense_content_frame:tk.Frame):
        '''Function to update an expense from the database by creating a new frame in the same window when called, 
        after clearing all the existing frames.it also has a vertical scroll feature fitting the exact length
        of the frame to accommodate all options. The frame also resizes approprialtely according to the window size
        args:
            expense_content_frame : 
        returns:
            None'''
        #clear existing frames before opening the update expense frame
        clear_content(expense_content_frame)
        # adding a vertical scroll 
        update_expense_canvas = tk.Canvas(expense_content_frame, bg="#c01010")
        update_expense_canvas.grid(row=0, column=0, sticky="nsew")
        update_expense_scrollbar = tk.Scrollbar(expense_content_frame, orient="vertical", command=update_expense_canvas.yview)
        update_expense_scrollbar.grid(row=0, column=1, sticky="ns")
        update_expense_frame = tk.Frame(update_expense_canvas, bg="#c01010", padx=10, pady=10)
        update_expense_canvas.configure(yscrollcommand=update_expense_scrollbar.set)
        update_expense_canvas.create_window((0, 0), window=update_expense_frame, anchor="nw")
        def on_configure(event):
            update_expense_canvas.configure(scrollregion=update_expense_canvas.bbox("all"))
            update_expense_canvas.itemconfig("all", width=event.width)
        update_expense_canvas.bind("<Configure>", on_configure)
        update_expense_frame .grid_columnconfigure(0, weight=1)
        update_expense_lbl = tk.Label(update_expense_frame, text="Update Expense", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
        update_expense_lbl.grid(row=0, column=0,pady=(10,0))

        update_expense_id_lbl = tk.Label(update_expense_frame, text="Update ID *", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_id_lbl.grid(row=2, column=0, pady=(20,0))
        update_expense_id_entry = tk.Entry(update_expense_frame, width=20, font=("Arial", 16), justify="center")
        update_expense_id_entry.grid(row=3, column=0, pady=(6,0))

        update_expense_date_lbl = tk.Label(update_expense_frame, text="Update date", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_date_lbl.grid(row=4, column=0, pady=(10,0))
        update_expense_date_check_btn_var = tk.BooleanVar(value=False)
        update_expense_date_check_btn = tk.Checkbutton(update_expense_frame, text="update date", font=("Arial", 16), bg="#c01010", fg="black", justify="center", variable=update_expense_date_check_btn_var, onvalue=True, offvalue=False)
        update_expense_date_check_btn.grid(row=5, column=0, pady=(2,0))
        update_expense_date_entry = DateEntry(update_expense_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 16), date_pattern='yyyy-mm-dd',justify="center")
        update_expense_date_entry.grid(row=6, column=0, pady=(6,0))

        update_expense_amount_lbl = tk.Label(update_expense_frame, text="Update amount", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_amount_lbl.grid(row=7, column=0, pady=(10,0))
        update_expense_amount_entry = tk.Entry(update_expense_frame, width=20, font=("Arial", 16), justify="center")
        update_expense_amount_entry.grid(row=8, column=0, pady=(6,0))

        update_expense_category_lbl = tk.Label(update_expense_frame, text="Update category", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_category_lbl.grid(row=9, column=0, pady=(10,0))
        update_expense_category_combobox = ttk.Combobox(update_expense_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
        update_expense_category_combobox.grid(row=10, column=0, pady=(6,0))

        update_expense_description_lbl = tk.Label(update_expense_frame, text="Update description", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_description_lbl.grid(row=11, column=0, pady=(10,0))
        update_expense_description_entry = tk.Entry(update_expense_frame, width=20, font=("Arial", 16), justify="center")
        update_expense_description_entry.grid(row=12, column=0, pady=(6,0))

        update_expense_payment_method_lbl = tk.Label(update_expense_frame, text="Update payment method", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        update_expense_payment_method_lbl.grid(row=13, column=0, pady=(10,0))
        update_expense_payment_method_combobox = ttk.Combobox(update_expense_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'], textvariable=tk.StringVar(), state="readonly", justify="center")
        update_expense_payment_method_combobox.grid(row=14, column=0, pady=(6,0))

        update_expense_check_btn_var = tk.BooleanVar(value=False)
        update_expense_check_btn = tk.Checkbutton(update_expense_frame, text=" Exceeding budget is fine", font=("Arial", 16), bg="#c01010", fg="black", justify="center", variable=update_expense_check_btn_var, onvalue=True, offvalue=False)
        update_expense_check_btn.grid(row=15, column=0, pady=(2,0))

        def submit_update_expense():
            '''Function to submit the updated expense to the database when called.
            args:
                None
            returns:
                None'''
            #None allows the user to skip updating a field, and modify only the desired fields
            try:
                expense_id = int(update_expense_id_entry.get())
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                return
            if update_expense_date_check_btn_var.get():
                date = update_expense_date_entry.get()
            else:
                date = None
            try:
                if update_expense_amount_entry.get() == "":
                    amount = None
                else:
                    amount = float(update_expense_amount_entry.get())
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                return
            category = update_expense_category_combobox.get()
            if category == "":
                category = None
            description = update_expense_description_entry.get()
            if description == "":
                description = None
            payment_method = update_expense_payment_method_combobox.get()
            if payment_method == "":
                payment_method = None
            valid,message = update_expense(expense_id, date, amount, category, description, payment_method)
            if valid:
                messagebox.showinfo("Success", message)
                update_expense_frame.destroy()
            else:
                messagebox.showerror("Error", message)
        update_expense_save_btn = tk.Button(update_expense_frame, text="Update Expense", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd=6, relief="raised", justify="center", command=submit_update_expense)
        update_expense_save_btn.grid(row=16, column=0, pady=(2,0))

def save_file_dialogue(file_name:str):
    ''' This function opens a file dialogue to allow the user to decide the file path and file name, 
    with a default file name as the one provided in the function argument. 
    The user can also change the file name and path in the dialogue box
    args:
        file_name (str): The default file name to be used in the dialogue box.
    returns:
        str: The file path and file name selected by the user.'''
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile=file_name, title="Save File", filetypes=(("csv files", "*.csv"),("All files", "*.*")))
    return file_path

def view_expenses_ui(view_expense_tuple:tuple, expense_content_frame:tk.Frame,file_name:str):
    '''Function to view all expenses from the database by creating a new frame in the same window when called.
    it uses ttk.Treeview to display the expenses in a tabular format with scrollbars.
    the column headers are id, date, amount, category, description, payment_method.
    the data is in the form of list of tuples where each tuple is a record
    displays each record in a seperate line under the respective header columns
    It also provides a button to export the expenses to a csv file,and returns a message box if the operation is successful or not.
    args:
        view_expense_tuple: A tuple containing the validity of the operation and the list of expenses.
        expense_content_frame: The frame where the view expenses frame will be created.
    returns:
        None'''
    clear_content(expense_content_frame)
    view_expenses_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    view_expenses_frame.grid(row=0, column=0, sticky="nsew")

    # Create a Treeview widget to display the expenses
    columns = ("id", "date", "amount", "category", "description", "payment_method")
    tree = ttk.Treeview(view_expenses_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    # Fetch expenses from the database
    valid,expenses = view_expense_tuple
    if valid:
        for expense in expenses:
            tree.insert("", tk.END, values=expense)
    else:
        messagebox.showerror("Error", "Failed to retrieve expenses.")
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(view_expenses_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky="ns")
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(view_expenses_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.grid(row=1, column=0, sticky="ew")
    # Place the Treeview widget
    tree.grid(row=0, column=0, sticky="nsew")
    view_expenses_frame.grid_rowconfigure(0, weight=1)
    view_expenses_frame.grid_columnconfigure(0, weight=1)
    #create a button to export the expenses to a csv file
    export_expenses_btn = tk.Button(view_expenses_frame, text="Export Expenses", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=lambda: export_expense_csv_ui())
    export_expenses_btn.grid(row=2, column=0, pady=(20,0))
    def export_expense_csv_ui():
        '''Function to export expenses from the database by creating a new frame in the same window when called.
        also checks if the write operation is successful or not.And returns a message box if the operation is successful or not.
        args:
            None
        returns:
            None'''
        # opens a file dialogue to allow the user to decide the file path and file name, with a default file name as the one provided in the function argument.
        file_path = save_file_dialogue(file_name)
        if not file_path:
            return
        valid = export_expense_csv(file_path,view_expense_tuple)
        if valid:
            messagebox.showinfo("Success", "Expenses exported successfully.")
        else:
            messagebox.showerror("Error", "Failed to export expenses.")

def search_expenses_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses from the database by creating a new frame in the same window when called.
    args:
        expense_content_frame: The frame where the search expenses frame will be created.
    returns:
        None'''
    #clearing all the existing frames before opening the search by expense ID frame
    clear_content(expense_content_frame)
    search_expense_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_expense_frame.grid(row=0, column=0, sticky="nsew")
    search_expense_frame.grid_columnconfigure(0, weight=1)

    search_expense_lbl = tk.Label(search_expense_frame, text="Search Expenses", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    search_expense_lbl.grid(row=0, column=0,pady=(10,0))

    search_expense_expid_btn = tk.Button(search_expense_frame, text="Search by Expense ID", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=lambda: search_expenses_expid_ui(expense_content_frame))
    search_expense_expid_btn.grid(row=1, column=0, pady=(20,0))

    search_expense_daterange_btn = tk.Button(search_expense_frame, text="Search by Date Range", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: search_expenses_daterange_ui(expense_content_frame))
    search_expense_daterange_btn.grid(row=2, column=0, pady=(20,0))

    search_expense_amountrange_btn = tk.Button(search_expense_frame, text="Search by Amount Range", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=lambda: search_expenses_amountrange_ui(expense_content_frame))
    search_expense_amountrange_btn.grid(row=3, column=0, pady=(20,0))

    search_expense_category_btn = tk.Button(search_expense_frame, text="Search by Category", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: search_expenses_category_ui(expense_content_frame))
    search_expense_category_btn.grid(row=4, column=0, pady=(20,0))


    search_expense_paymentmethod_btn = tk.Button(search_expense_frame, text="Search by Payment Method", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=lambda: search_expenses_paymentmethod_ui(expense_content_frame))
    search_expense_paymentmethod_btn.grid(row=5, column=0, pady=(20,0))

def search_expenses_daterange_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses by date range.
    args:
        expense_content_frame: the frame where the search expenses frame will be created.
    returns:
        None'''
    #clear all the the existing frames before opening the search by date range frame
    clear_content(expense_content_frame)
    search_daterange_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_daterange_frame.grid(row=0, column=0, sticky="nsew")
    search_daterange_frame.grid_columnconfigure(0, weight=1)

    start_date_lbl = tk.Label(search_daterange_frame, text="Start Date:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    start_date_lbl.grid(row=1, column=0, pady=(10, 0))

    start_date_entry = DateEntry(search_daterange_frame, font=("Arial", 20), bg="white", fg="black", date_pattern='yyyy-mm-dd', justify="center")
    start_date_entry.grid(row=2, column=0, pady=(6, 0))

    end_date_lbl = tk.Label(search_daterange_frame, text="End Date:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    end_date_lbl.grid(row=3, column=0, pady=(10, 0))

    end_date_entry = DateEntry(search_daterange_frame, font=("Arial", 20), bg="white", fg="black", date_pattern='yyyy-mm-dd', justify="center")
    end_date_entry.grid(row=4, column=0, pady=(6, 0))
    search_btn = tk.Button(search_daterange_frame, text="Search", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command= lambda: view_expenses_ui(search_expenses(date_range=(start_date_entry.get(),end_date_entry.get())), expense_content_frame,"expenses_date_range.csv"))
    search_btn.grid(row=5, column=0, pady=(20, 0))

def search_expenses_amountrange_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses by amount range.
    args:
        expense_content_frame: the frame where the search expenses frame will be created.
    returns:
        None'''
    #clear all the the existing frames before opening the search by amount range frame
    clear_content(expense_content_frame)
    search_amountrange_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_amountrange_frame.grid(row=0, column=0, sticky="nsew")
    search_amountrange_frame.grid_columnconfigure(0, weight=1)

    min_amount_lbl = tk.Label(search_amountrange_frame, text="Minimum Amount:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    min_amount_lbl.grid(row=1, column=0, pady=(10, 0))
    min_amount_entry = tk.Entry(search_amountrange_frame, font=("Arial", 20), bg="white", fg="black", justify="center")
    min_amount_entry.grid(row=2, column=0, pady=(6, 0))

    max_amount_lbl = tk.Label(search_amountrange_frame, text="Maximum Amount:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    max_amount_lbl.grid(row=3, column=0, pady=(10, 0))
    max_amount_entry = tk.Entry(search_amountrange_frame, font=("Arial", 20), bg="white", fg="black", justify="center")
    max_amount_entry.grid(row=4, column=0, pady=(6, 0))

    search_btn = tk.Button(search_amountrange_frame, text="Search", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command= lambda: view_expenses_ui(search_expenses(amount_range=(min_amount_entry.get(), max_amount_entry.get())), expense_content_frame,"expenses_amount_range.csv"))
    search_btn.grid(row=5, column=0, pady=(20, 0))

def search_expenses_category_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses by category.
    args:
        expense_content_frame: the frame where the search expenses frame will be created.
    returns:
        None'''
    # clearing all the existing frames before opening the search by category frame
    clear_content(expense_content_frame)
    search_category_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_category_frame.grid(row=0, column=0, sticky="nsew")
    search_category_frame.grid_columnconfigure(0, weight=1)
    category_lbl = tk.Label(search_category_frame, text="Category:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    category_lbl.grid(row=1, column=0, pady=(10, 0))
    category_combobox = ttk.Combobox(search_category_frame, width=20, font=("Arial", 16), values=constants['valid_categories'],textvariable=tk.StringVar(), state="readonly",justify="center")
    category_combobox.grid(row=2, column=0, pady=(6, 0))

    search_btn = tk.Button(search_category_frame, text="Search", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_expenses_ui(search_expenses(category=category_combobox.get()), expense_content_frame,"expenses_category.csv"))
    search_btn.grid(row=3, column=0, pady=(20, 0))

def search_expenses_paymentmethod_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses by payment method.
    args:
        expense_content_frame: the frame where the search expenses frame will be created.
    returns:
        None'''
    # clearing all the existing frames before opening the search by payment method frame
    clear_content(expense_content_frame)
    search_paymentmethod_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_paymentmethod_frame.grid(row=0, column=0, sticky="nsew")
    search_paymentmethod_frame.grid_columnconfigure(0, weight=1)
    payment_method_lbl = tk.Label(search_paymentmethod_frame, text="Payment Method:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    payment_method_lbl.grid(row=1, column=0, pady=(10, 0))
    payment_method_combobox = ttk.Combobox(search_paymentmethod_frame, width=20, font=("Arial", 16), values=constants['valid_payment_methods'],textvariable=tk.StringVar(), state="readonly",justify="center")
    payment_method_combobox.grid(row=2, column=0, pady=(6, 0))

    search_btn = tk.Button(search_paymentmethod_frame, text="Search", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_expenses_ui(search_expenses(payment_method=payment_method_combobox.get()), expense_content_frame,"expenses_payment_method.csv"))
    search_btn.grid(row=3, column=0, pady=(20, 0))

def search_expenses_expid_ui(expense_content_frame:tk.Frame):
    '''Function to search expenses by expense ID.
    args:
        expense_content_frame: the frame where the search expenses frame will be created.
    returns:
        None'''
    # clearing all the existing frames before opening the search by expense ID frame
    clear_content(expense_content_frame)
    search_expid_frame = tk.Frame(expense_content_frame, padx=10, pady=10, bg="#c01010")
    search_expid_frame.grid(row=0, column=0, sticky="nsew")
    search_expid_frame.grid_columnconfigure(0, weight=1)
    expense_id_lbl = tk.Label(search_expid_frame, text="Expense ID:", font=("Arial", 20, "bold"), bg="#c01010", fg="white")
    expense_id_lbl.grid(row=1, column=0, pady=(10, 0))
    expense_id_entry = tk.Entry(search_expid_frame, font=("Arial", 20), bg="white", fg="black", justify="center")
    expense_id_entry.grid(row=2, column=0, pady=(6, 0))
    
    search_btn = tk.Button(search_expid_frame, text="Search", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=lambda: view_expenses_ui(get_expense_by_id(expense_id_entry.get()),expense_content_frame,"expenses_id.csv"))
    search_btn.grid(row=3, column=0, pady=(20, 0))