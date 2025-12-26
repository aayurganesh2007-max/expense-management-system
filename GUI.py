import tkinter as tk
from tkcalendar import Calendar, DateEntry
#from database import add_expense, delete_expense, update_expense, view_expenses, export_expenses, search_expenses
window = tk.Tk()
window.title("Expense Manager")
window.geometry("800x600")

# Configure the grid to allow the cell to expand with the window
# This is important so that "center" has meaning relative to the whole window
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a frame to hold the content
frame = tk.Frame(window, padx=10, pady=10, bg="#9c0b0b")
frame.grid(row=0, column=0, sticky="nsew")

# Configure the frame to expand within the cell
# This is important so that "center" has meaning relative to the frame
#frame.grid_rowconfigure(1, weight=1) #by giving the weight to Row 1 (which is empty), that row will take all the extra space
frame.grid_columnconfigure(0, weight=1)

# Add the top label
top_lbl = tk.Label(frame, text="EXPENSE MANAGER", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
top_lbl.grid(row=0, column=0,pady=10)

expense_lbl = tk.Label(frame, text="Manage your expenses", font=("Arial", 28, "bold"), bg="#0ba8d4", fg="black", bd = 3, relief="solid", justify="center")
expense_lbl.grid(row=1, column=0, pady=(50,0))#the tuple ensures that there is more padding on top than bottom

def open_expense_window():
    '''Function to open the expense management window and operate on this window with different frames and widgets.
    args:
        None
    returns:
        None'''
    new_expense_window = tk.Toplevel(window)
    new_expense_window.title("Expense Management")
    new_expense_window.geometry("800x600")
    new_expense_window.grid_rowconfigure(0, weight=1)
    new_expense_window.grid_columnconfigure(0, weight=1)

    expense_frame = tk.Frame(new_expense_window, padx=10, pady=10, bg="#9c0b0b")
    expense_frame.grid(row=0, column=0, sticky="nsew")
    expense_frame.grid_columnconfigure(0, weight=1)
    expense_lbl = tk.Label(expense_frame, text="Expense Management Window", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
    expense_lbl.grid(row=0, column=0,pady=(10,0))

    def new_expense():
        '''Function to add a new expense to the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        expense_frame.grid_forget()
        new_expense_frame = tk.Frame( padx=10, pady=10, bg="#9c0b0b")
        new_expense_frame.grid(row=0, column=1, sticky="nsew")
        new_expense_frame.grid_columnconfigure(0, weight=1)

        new_expense_lbl = tk.Label(new_expense_frame, text="Add New Expense", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
        new_expense_lbl.grid(row=0, column=0,pady=(10,0))

        new_date_lbl = tk.Label(new_expense_frame, text="Date:", font=("Arial", 20, "bold"), bg="#0ae2d0", fg="black", bd = 3, relief="solid", justify="center")
        new_date_lbl.grid(row=1, column=0, pady=(20,0))

        new_date_entry = DateEntry(new_expense_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 16), date_pattern='dd/mm/yyyy')
        new_date_entry.grid(row=2, column=0, pady=(10,0))

        
    new_expense_btn = tk.Button(expense_frame, text="Add New Expense", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=new_expense)
    new_expense_btn.grid(row=2, column=0, pady=(10,0))

    def delete_expense():
        '''Function to delete an expense from the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        
        pass
    delete_expense_btn = tk.Button(expense_frame, text="Delete Expense", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=delete_expense)
    delete_expense_btn.grid(row=3, column=0, pady=(10,0))

    def update_expense():
        '''Function to update an expense from the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        pass
    update_expense_btn = tk.Button(expense_frame, text="Update Expense", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=update_expense)
    update_expense_btn.grid(row=4, column=0, pady=(10,0))

    def view_expenses():
        '''Function to view all expenses from the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        pass
    view_expenses_btn = tk.Button(expense_frame, text="View Expenses", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=view_expenses)
    view_expenses_btn.grid(row=5, column=0, pady=(10,0))

    def export_expenses():
        '''Function to export expenses from the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        pass
    export_expenses_btn = tk.Button(expense_frame, text="Export Expenses", font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd=6, relief="raised", justify="center", command=export_expenses)
    export_expenses_btn.grid(row=6, column=0, pady=(10,0))

    def search_expenses():
        '''Function to search expenses from the database by creating a new frame in the same window when called.
        args:
            None
        returns:
            None'''
        pass
    search_expenses_btn = tk.Button(expense_frame, text="Search Expenses", font=("Arial", 20, "bold"), bg="#0398fc", fg="black", bd=6, relief="raised", justify="center", command=search_expenses)
    search_expenses_btn.grid(row=7, column=0, pady=(10,0))


    expense_destroy_btn = tk.Button(expense_frame, text="Close", font=("Arial", 20, "bold"), bg="#ff0000", fg="white", bd=6, relief="raised", justify="center", command=new_expense_window.destroy)
    expense_destroy_btn.grid(row=8, column=0, pady=(10,0))

expense_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd = 6, relief="raised", justify="center", command=open_expense_window)
expense_btn .grid(row=2, column=0 )
budget_lbl = tk.Label(frame, text="Set your budgets", font=("Arial", 28, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
budget_lbl.grid(row=3, column=0, pady=(20,0))#the tuple ensures that there is more padding on top than bottom

budget_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 6, relief="raised", justify="center")
budget_btn.grid(row=4, column=0 )

visualize_lbl = tk.Label(frame, text="Visualize your analytics", font=("Arial", 28, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
visualize_lbl.grid(row=5, column=0, pady=(20,0))#the tuple ensures that there is more padding on top than bottom
visualize_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#e38c0a", fg="black", bd = 6, relief="raised", justify="center")
visualize_btn.grid(row=6, column=0 )

window.mainloop()