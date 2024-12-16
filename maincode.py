import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os
import hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Root Window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")
root.configure(bg="#f4f4f9")

# Global Styles
BG_COLOR = "#f4f4f9"
FG_COLOR = "#333"
BTN_COLOR = "#4CAF50"
BTN_TEXT_COLOR = "white"
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_BODY = ("Arial", 12)
FONT_BUTTON = ("Arial", 12, "bold")

# User Data
current_user = None
users = {}
expenses = []

# Helper Functions
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def navigation_bar():
    nav_frame = tk.Frame(root, bg="#333")
    nav_frame.pack(fill="x")

    nav_buttons = [
        ("Home", home_page),
        ("Add Expense", add_expense_page),
        ("View Expenses", view_expenses_page),
        ("Summary", summary_page),
        ("Logout", logout)
    ]

    for text, command in nav_buttons:
        tk.Button(
            nav_frame, text=text, command=command, font=FONT_BODY,
            bg="#4CAF50", fg="white", relief="flat", width=12, cursor="hand2"
        ).pack(side="left", padx=5, pady=5)

# Load users from a CSV file
def load_users():
    global users
    users = {}
    if os.path.exists('users.csv'):
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle cases where 'Email' might be missing
                email = row.get("Email", "")  # Default to empty string if 'Email' is missing
                users[row["Username"]] = {"Username": row["Username"], "Password": row["Password"], "Email": email}

# Save users to CSV
def save_users():
    with open('users.csv', mode='w', newline='') as file:
        fieldnames = ["Username", "Password", "Email"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

# Save expenses to CSV
def save_expenses():
    with open(f'{current_user}_expenses.csv', mode='w', newline='') as file:
        fieldnames = ["Date", "Category", "Amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)

# Load expenses from CSV for the current user
def load_expenses_for_user():
    global expenses
    expenses = []
    if os.path.exists(f'{current_user}_expenses.csv'):
        with open(f'{current_user}_expenses.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({"Date": row["Date"], "Category": row["Category"], "Amount": row["Amount"]})

# Hash the password for storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate user credentials
def login_user(username, password):
    load_users()
    hashed_password = hash_password(password)
    if username in users and users[username]["Password"] == hashed_password:
        global current_user
        current_user = username
        load_expenses_for_user()  # Load expenses for the current user
        home_page()  # Go to the home page after successful login
        return True
    else:
        messagebox.showerror("Error", "Invalid username or password.")
        return False

# Register new user
def register_user(username, password, email):
    if username in users:
        messagebox.showerror("Error", "Username already exists.")
        return
    hashed_password = hash_password(password)
    users[username] = {"Username": username, "Password": hashed_password, "Email": email}
    save_users()
    messagebox.showinfo("Success", "User registered successfully! You can now log in.")
    login_page()  # Switch to login page after registration

# Pages
def home_page():
    clear_window()
    
    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    navigation_bar()

    # User Details
    user_frame = tk.Frame(root, bg=BG_COLOR)
    user_frame.pack(pady=20)

    tk.Label(user_frame, text="User Details", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    if current_user:
        user_details = {
            "Name": current_user,
            "Email": users[current_user]["Email"]
        }

        for key, value in user_details.items():
            tk.Label(user_frame, text=f"{key}: {value}", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w", padx=20)

    # Logout Button
    tk.Button(
        root, text="Logout", command=logout, font=FONT_BUTTON,
        bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def login_page():
    clear_window()

    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    # Username and Password Inputs
    tk.Label(root, text="Username", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    username_entry = tk.Entry(root, font=FONT_BODY)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    password_entry = tk.Entry(root, font=FONT_BODY, show="*")
    password_entry.pack(pady=5)

    # Show Password Checkbox
    def toggle_password():
        if password_entry.cget('show') == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    show_password_checkbox = tk.Checkbutton(root, text="Show Password", bg=BG_COLOR, fg=FG_COLOR, font=FONT_BODY, command=toggle_password)
    show_password_checkbox.pack(pady=5)

    def on_login_submit():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            login_user(username, password)
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    # Login Button
    tk.Button(
        root, text="Login", command=on_login_submit, font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
        width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

    # Register Button
    def on_signup():
        signup_page()

    tk.Button(
        root, text="Sign Up", command=on_signup, font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
        width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def signup_page():
    clear_window()

    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    # Username, Password, Email Inputs
    tk.Label(root, text="Username", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    username_entry = tk.Entry(root, font=FONT_BODY)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    password_entry = tk.Entry(root, font=FONT_BODY, show="*")
    password_entry.pack(pady=5)

    tk.Label(root, text="Email", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    email_entry = tk.Entry(root, font=FONT_BODY)
    email_entry.pack(pady=5)

    # Show Password Checkbox
    def toggle_password():
        if password_entry.cget('show') == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    show_password_checkbox = tk.Checkbutton(root, text="Show Password", bg=BG_COLOR, fg=FG_COLOR, font=FONT_BODY, command=toggle_password)
    show_password_checkbox.pack(pady=5)

    def on_signup_submit():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        if username and password and email:
            register_user(username, password, email)
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Register Button
    tk.Button(
        root, text="Sign Up", command=on_signup_submit, font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
        width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

    # Login Button
    def on_login():
        login_page()

    tk.Button(
        root, text="Login", command=on_login, font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
        width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def add_expense_page():
    clear_window()
    
    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    navigation_bar()

    # Expense Form
    tk.Label(root, text="Add Expense", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

    tk.Label(root, text="Date", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    date_entry = DateEntry(root, font=FONT_BODY)
    date_entry.pack(pady=5)

    tk.Label(root, text="Category", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    category_entry = tk.Entry(root, font=FONT_BODY)
    category_entry.pack(pady=5)

    tk.Label(root, text="Amount", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    amount_entry = tk.Entry(root, font=FONT_BODY)
    amount_entry.pack(pady=5)

    def on_add_expense():
        date = date_entry.get()
        category = category_entry.get()
        amount = amount_entry.get()
        if date and category and amount:
            expenses.append({"Date": date, "Category": category, "Amount": amount})
            save_expenses()
            messagebox.showinfo("Success", "Expense added successfully!")
            home_page()
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Add Expense Button
    tk.Button(
        root, text="Add Expense", command=on_add_expense, font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
        width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def view_expenses_page():
    clear_window()

    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    navigation_bar()

    tk.Label(root, text="View Expenses", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

    columns = ("Date", "Category", "Amount")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.pack(pady=20)

    for col in columns:
        tree.heading(col, text=col)

    for expense in expenses:
        tree.insert("", tk.END, values=(expense["Date"], expense["Category"], expense["Amount"]))

    # Back Button
    def back_to_home():
        home_page()

    tk.Button(
        root, text="Back", command=back_to_home, font=FONT_BUTTON,
        bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def summary_page():
    clear_window()
    
    # Title
    title_label = tk.Label(root, text="Expense Tracker", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
    title_label.pack(pady=20)

    navigation_bar()

    tk.Label(root, text="Summary", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

    total = sum(float(expense["Amount"]) for expense in expenses)
    tk.Label(root, text=f"Total Expenses: ${total:.2f}", font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

    # Plot the Summary Graph
    categories = {}
    for expense in expenses:
        category = expense["Category"]
        amount = float(expense["Amount"])
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories.keys(), categories.values())
    ax.set_xlabel('Category')
    ax.set_ylabel('Amount (Rs)')
    ax.set_title('Expenses by Category')

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().pack(pady=20)
    canvas.draw()

    # Back Button
    def back_to_home():
        home_page()

    tk.Button(
        root, text="Back", command=back_to_home, font=FONT_BUTTON,
        bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=18, height=2, relief="flat", cursor="hand2"
    ).pack(pady=20)

def logout():
    global current_user
    current_user = None
    login_page()

# Start with the login page
login_page()

root.mainloop()
