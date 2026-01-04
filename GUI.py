import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import  DateEntry
from constant import constants
from expense_gui import open_expense_window,clear_content,new_expense,delete_expense_ui,update_expense_ui,view_expenses_ui,search_expenses_ui,search_expenses_expid_ui,search_expenses_daterange_ui,search_expenses_amountrange_ui,search_expenses_category_ui,search_expenses_paymentmethod_ui
from budget_gui import open_budget_window,new_budget_ui
from visualizations_gui import open_visualizations_window

#from database import add_expense, delete_expense, update_expense, view_expenses, export_expenses, search_expenses
window = tk.Tk()
window.title("Expense Manager")
window.geometry("800x700")


# Configure the grid to allow the cell to expand with the window
# This is important so that "center" has meaning relative to the whole window
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a frame to hold the content
frame = tk.Frame(window, padx=10, pady=10, bg="#9c0b0b")
frame.grid(row=0, column=0, sticky="nsew")

# Configure the frame to expand within the cell
# This is important so that "center" has meaning relative to the frame
#frame.grid_rowconfigure(0, weight=1) #by giving the weight to Row 1 (which is empty), that row will take all the extra space
frame.grid_columnconfigure(0, weight=1)

# Add the top label
top_lbl = tk.Label(frame, text="EXPENSE MANAGER", font=("Arial", 36, "bold"), bg="#ebd409", fg="Black", bd = 5, relief="ridge", justify="center")
top_lbl.grid(row=0, column=0,pady=10)

expense_lbl = tk.Label(frame, text="Manage your expenses", font=("Arial", 28, "bold"), bg="#0ba8d4", fg="black", bd = 3, relief="solid", justify="center")
expense_lbl.grid(row=1, column=0, pady=(40,0))#the tuple ensures that there is more padding on top than bottom
expense_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#0ad4b6", fg="black", bd = 6, relief="raised", justify="center", command=lambda: open_expense_window(window))
expense_btn .grid(row=2, column=0 )

budget_lbl = tk.Label(frame, text="Set your budgets", font=("Arial", 28, "bold"), bg="#1aab0a", fg="black", bd = 3, relief="solid", justify="center")
budget_lbl.grid(row=3, column=0, pady=(20,0))#the tuple ensures that there is more padding on top than bottom
budget_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#61cc0a", fg="black", bd = 6, relief="raised", justify="center",command=lambda: open_budget_window(window))
budget_btn.grid(row=4, column=0 )

visualize_lbl = tk.Label(frame, text="Visualize your analytics", font=("Arial", 28, "bold"), bg="#e94c0e", fg="black", bd = 3, relief="solid", justify="center")
visualize_lbl.grid(row=5, column=0, pady=(20,0))#the tuple ensures that there is more padding on top than bottom
visualize_btn = tk.Button(frame, text = 'Enter', font=("Arial", 20, "bold"), bg="#e38c0a", fg="black", bd = 6, relief="raised", justify="center",command=lambda: open_visualizations_window(window))
visualize_btn.grid(row=6, column=0)

def safe_action():
    ''' In case there is an error in the processing the user interface, 
    and displays the error message to the user and closes the window.
    args:
        None
    returns:
        None'''
    try:
        
window.mainloop()