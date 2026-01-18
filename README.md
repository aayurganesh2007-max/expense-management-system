Expense Management System

A "desktop-based Expense Management System" built using Python,Tkinter, SQLite, and Matplotlib, designed to help users track expenses, manage budgets, search records, and visualize financial data through an intuitive GUI.
This project was developed as part of a Databased Fall of Code(DFOC-2025), with a strong focus on clean design, robustness, and realworld usability.

Core Features:

1)Expense Management-
-Add, update, delete, and search expenses
-Category‑wise expense tracking
-Multiple payment methods support
-Robust validation with clear error feedback

2) Budget Management-
-Define monthly budgets per category
-View all budgets together
-Budget vs actual comparison
-Handles partial or missing budgets gracefully

3)Data Visualization & Analytics:
-Bar Charts – Monthly expense summaries
-Line Graphs – Expense trends (e.g. food expense fluctuation)
-Pie Charts – Category‑wise distribution
-Double Bar Charts – Budget vs actual comparison
-Visualizations handle empty or sparse data without crashing

GUI (Tkinter):
-Modular window layout
-Resizable windows
-Comboboxes, calendar widgets, scrollable tables
-Embedded Matplotlib figures inside Tkinter
-File dialogs for CSV imports

Project Structure:
expense-management-system/
│
├── main.py                 # Main entry point (run this)
│
├── expense_gui.py          # Expense-related GUI logic
├── budget_gui.py           # Budget-related GUI logic
├── visualizations_gui.py   # Analytics & charts GUI
│
├── expense.py              # Expense business logic
├── budget.py               # Budget business logic
├── analytics.py            # Data aggregation for charts
│
├── database.py             # Database operations
├── connection.py           # Safe DB connection handling
│
├── validators.py           # Input validation
├── constants.py            # Categories, months, payment methods
│
├── expense.db              # SQLite database (auto-created)
│
└── README.md

Install dependencies-
pip install tkcalender
pip install pandas
pip install matplotlib

Note: "main.py" is the single official entry point of the application.

Important Design Decisions:
Defensive programming with validations at multiple layers
Graceful handling of:
 -Empty databases
 -Missing months or categories
 -Partial budgets
Try/except used only at meaningful boundaries, not deeply nested
Centralized constants to avoid duplication and inconsistency

Future Improvements:
Savings tracking
User authentication & multi‑user support
Personalized analytics & insights
PDF report exports
Chart export as images

Learning Outcomes

Through this project, I gained hands-on experience with:
-Importance of defensive programming
-Designing clean module boundaries
- Handling real‑world imperfect data
-Integrating multiple Python libraries into a cohesive system

Final note:
this project gave me practical experience in building a complete application rather than isolated features. I focused on robustness, input validation, and clear separation between the GUI and database logic. It also helped me understand how multiple libraries like SQLite, Pandas, Matplotlib, and Tkinter work together in a real system. The current version is stable and functional, and the project gave me a much clearer idea of how to design maintainable software
