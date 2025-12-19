from expense import add_expense
from budget import set_update_monthly_budget,set_update_monthly_category_budget,set_update_monthly_payment_method_budget
constants = {'valid_categories': ['food', 'transport', 'utilities', 'entertainment', 'miscellaneous'],
    'valid_payment_methods': ['cash','upi','credit card', 'debit card', 'netbanking','wallet']
}
sample_expenses = [
    ("2024-01-05", 250, "food","Lunch", "upi" ),
    ("2024-01-10", 1200, "transport","Train pass", "debit card"),
    ("2024-01-15", 500, "entertainment","Movie","upi"),
    ("2024-02-03", 300, "food","Snacks", "cash"),
    ("2024-02-14", 2200, "utilities", "Clothes","credit card" ),
    ("2024-03-01", 1500, "utilities", "Room rent", "upi"),
    ("2024-03-12", 450, "food", "Dinner", "upi"),
    ("2024-03-18", 700, "Transport", "cash",'cab'),
    ("2024-04-05", 2000, "utilities", "Books", "debit card"),
    ("2024-04-22", 600, "entertainment","Concert", "upi" ),
]
for data in sample_expenses:
    add_expense(*data)

monthly_budgets = [
    (2024, 1, 8000),
    (2024, 2, 7500),
    (2024, 3, 9000),
    (2024, 4, 8500),
]
for data in monthly_budgets:
    set_update_monthly_budget(*data)

category_budgets = [
    (2024, 3, "food", 3000),
    (2024, 3, "utilities", 2000),
    (2024, 3, "transport", 1500),
    (2024, 3, "entertainment", 1000),
    (2024, 3, "miscellaneous", 1500),
]

for data in category_budgets:
    set_update_monthly_category_budget(*data)

payment_method_budgets = [
    (2024, 3, "upi", 4000),
    (2024, 3, "debit card", 3500),
    (2024, 3, "cash", 1500),
]

for data in payment_method_budgets:
    set_update_monthly_payment_method_budget(*data)

