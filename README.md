# 📊 Expense Management System

A **desktop-based Expense Management System** built using **Python, Tkinter, SQLite, and Matplotlib**, designed to help users **track expenses, manage budgets, search records, and visualize financial data** through an intuitive GUI.

This project was developed as part of a **coding club project(DFOC-2025)**,  with a strong focus on **clean design, robustness, and real-world usability**.

---

## ✨ Features

### 🧾 Expense Management

* Add new expenses with:

  * Date
  * Amount
  * Category
  * Description
  * Payment method
* Delete expenses using Expense ID
* Update expenses (supports partial updates — empty fields are ignored)
* View all expenses in a structured table

### 🔍 Advanced Search

Search expenses by:

* Expense ID
* Date range
* Amount range
* Category
* Payment method

Each search result can be:

* Viewed directly in the GUI
* Exported to CSV

### 💰 Budget Management

* Set monthly budgets
* View budgets by:

  * Month
  * Category
  * Payment method
* Compare expenses against budgets

### 📈 Data Visualization

Interactive analytics using **Matplotlib**, embedded inside Tkinter:

* Monthly expense bar charts
* Daily expense line graphs
* Category-wise expense distribution
* Budget vs Expense comparisons

All visualizations handle:

* Empty datasets
* Fresh installs
* Missing months safely

### 📤 Export Functionality

* Export expenses and search results to **CSV**
* User-controlled save location via file dialog
* Safe overwrite handling

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **GUI:** Tkinter
* **Database:** SQLite
* **Charts & Analytics:** Matplotlib
* **Calendar Input:** tkcalendar
* **Data Handling:** Custom validation & database wrappers

---

## 📂 Project Structure

```
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
```

---

## ▶️ How to Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/aayurganesh2007-max/expense-management-system.git
cd expense-management-system
```

### 2️⃣ Install dependencies

```bash
pip install tkcalendar matplotlib
```

### 3️⃣ Run the application

```bash
python main.py
```

> ⚠️ **Important:**
> `main.py` is the **single official entry point** of the application.

---

## 🧠 Design Decisions & Best Practices

### ✅ Robust Error Handling

* No unsafe `assert` usage
* All database operations return `(bool, data/message)`
* GUI actions catch runtime errors and display user-friendly messages

### ✅ Safe Database Access

* Context-managed database connections
* Graceful handling of:

  * Empty databases
  * Missing data
  * Fresh installs

### ✅ GUI Stability

* Errors never crash the app
* All failures are reported via dialog boxes
* Input validation handled before DB operations

### ✅ Extensible Architecture

* Clear separation between:

  * GUI
  * Business logic
  * Database layer
* Easy to add:

  * New analytics
  * Export formats (PDF planned)
  * Authentication (future)

---

## 🚀 Future Improvements

* PDF export support
* Charts export as images
* Undo/Redo for expense edits
* User profiles & authentication
* MVC-based refactoring
* Automated tests

---

## 🎓 Learning Outcomes

Through this project, I gained hands-on experience with:

* GUI design using Tkinter
* SQLite database design & safety
* Error handling and defensive programming
* Data visualization integration
* Writing clean, readable, maintainable code

---

## 👤 Author

**Aayur Ganesh**
Coding Club Project – Expense Management System

---
## 🤖 AI Assistance Disclosure

AI tools were used only for **code review and design feedback**, not for writing code.  
All implementation, debugging, and integration were done manually by the author.


## ⭐ Final Notes

This project prioritizes **correctness, stability, and clarity** over unnecessary complexity, making it suitable for **real-world usage and academic evaluation**.

---


