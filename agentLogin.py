import tkinter as tk
from tkinter import messagebox

def AgentLoginWindow(parent_window):
    loginWindow = tk.Toplevel(parent_window, bg="blue")
    loginWindow.title("Agent Login")
    loginWindow.geometry("300x200")
    
    tk.Label(loginWindow, text="Username:", bg="blue", fg="white").pack(pady=10)
    usernameInput = tk.Entry(loginWindow)
    usernameInput.pack(pady=5)
    
    tk.Label(loginWindow, text="Password:", bg="blue", fg="white").pack(pady=10)
    passwordInput = tk.Entry(loginWindow, show="*")
    passwordInput.pack(pady=5)
    
    tk.Button(loginWindow, text="Login", command=lambda: login(usernameInput.get(), passwordInput.get())).pack(pady=10)

def login(username, password):
    # Replace with your authentication logic (e.g., database lookup)
    if username == "agent" and password == "agent123":
        messagebox.showinfo("Login Successful", "Welcome, Agent!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
