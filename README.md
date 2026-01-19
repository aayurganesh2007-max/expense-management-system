**Expense Management System**

A "An Expense Management System" built using Python,Tkinter, SQLite, Pandas and Matplotlib, designed to help users track expenses, manage budgets, search records, and visualize financial data through an robust and simple GUI (made using Tkinter).
This project was developed as part of a Databased Fall of Code ( DFOC-2025 ), with a strong focus on clean design, robustness, realworld usability and scalabilty
<img width="700" height="650" alt="image" src="https://github.com/user-attachments/assets/dd5d95cf-dca3-4680-8302-dcc1be7027f3" />


<img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/58340f51-1136-439a-8a88-ed3c717e266d" /> 

<img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/fe110f92-1296-4824-b203-9871be44a10b" />

<img width="550" height="450" alt="image" src="https://github.com/user-attachments/assets/bde3e056-ee4b-484b-9c22-35f4708e753f" />

* **Core Features:**
  - Expense Management:
    - Add, update, delete, and search expenses
    - View and export expenses to CSV
    - Category‑wise expense tracking
    - Multiple payment methods support
    - Robust validation with clear error feedback     
      
  - Budget Management:
    - Define monthly budgets
    - Define monthly per category budgets
    - Define monthly per payment method budgets
    - Add, update, and delete budget entries
    - View all budgets together and export to CSV
    - Handles partial or missing budgets gracefully    

  - Data Visualization & Analytics:
    - Bar Charts – Monthly expense summaries
    - Line Graphs – Daily expense trend
    - Pie Charts – Category‑wise distribution
    - Double Bar Charts – Budget vs actual comparison
    - Visualizations handle empty or sparse data without crashing

  - GUI (Tkinter):
    - Modular window layout
    - Resizable windows
    - Comboboxes, calendar widgets, scrollable tables, messageboxes
    - Embedded Matplotlib figures inside Tkinter
    - File dialogs for CSV imports

* **Project Structure:**
  - expense-management-system
    - main.py                 (Main entry point)

    - expense_gui.py          (Expense-related GUI logic)
    - budget_gui.py           (Budget-related GUI logic)
    - visualizations_gui.py   (Analytics & charts GUI)

    - expense.py              (Expense business logic)
    - budget.py               (Budget business logic)
      
    - analytics.py            (Data aggregation for charts)

    - visualizations.py       (Data visualizations - graphs and charts)
   
    - database_connections.py (Safe DB connection handling)
    - validators.py           (Input validation)
    - constants.py            (Categories, months, payment methods)
   
    - expense.db              (SQLite database for expense)
    - budget.db               (SQLite database for budget)

    - README.md

* **Install dependencies**:
  - Run these on the terminal on by one 
  ```
  pip install tkcalender
  ```
  ```
  pip install pandas
  ```
  ```
  pip install matplotlib
  ```

* **Important Design Decisions:**
  - Seperate files for eacch responsibilty
  - Defensive programming with validations at multiple layers
  - Graceful handling of:
    - Empty databases
    - Missing months or categories
    - Partial budgets
  - Try/except used only at meaningful boundarie
  - Centralized constants to avoid duplication and inconsistency
  

* **Future Improvements:**
  - Savings tracking
  - User authentication & multi‑user support
  - Personalized analytics & insights
  - PDF report exports
  - Chart export as images

* **Learning Outcomes**
  - Through this project, I gained hands-on experience with:
    - Importance of defensive programming
    - Designing clean module boundaries
    - Handling real‑world imperfect data
    - Seperation of concerns
    - User interface interaction with the backend logic
    - Integrating multiple Python libraries into a cohesive system
