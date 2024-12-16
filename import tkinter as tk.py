import tkinter as tk
from tkinter import messagebox

def login():
    
    email = email_var.get()
    password = password_var.get()

    
    if not email or not password:
        messagebox.showerror("Error", "Both fields are required!")
        return

    
    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                saved_name, saved_email, saved_password = user.strip().split(",")
                if email == saved_email and password == saved_password:
                    messagebox.showinfo("Success", f"Welcome back, {saved_name}!")
                    return
            messagebox.showerror("Error", "Invalid email or password!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No registered users found!")


root = tk.Tk()
root.title("Login Page")
root.geometry("300x200")

email_var = tk.StringVar()
password_var = tk.StringVar()


tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Email:").pack(anchor="w", padx=20)
tk.Entry(root, textvariable=email_var).pack(fill="x", padx=20, pady=5)

tk.Label(root, text="Password:").pack(anchor="w", padx=20)
tk.Entry(root, textvariable=password_var, show="*").pack(fill="x", padx=20, pady=5)


tk.Button(root, text="Login", command=login, bg="green", fg="white").pack(pady=20)


root.mainloop()
