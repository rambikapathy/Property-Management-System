import tkinter as tk
from tkinter import messagebox
import sqlite3
from propertyWindow import openPropertyWindow

def AgentLoginWindow(parent_window):
    loginWindow = tk.Toplevel(parent_window, bg="black")
    loginWindow.title("Agent Login")
    loginWindow.geometry("400x250")
    loginWindow.resizable(False, False)

    conn = sqlite3.connect('agents.db')
    c = conn.cursor()

    tk.Label(loginWindow, text="Username:", bg="black", fg="white").pack(pady=10)
    usernameInput = tk.Entry(loginWindow)
    usernameInput.pack(pady=5)

    tk.Label(loginWindow, text="Password:", bg="black", fg="white").pack(pady=10)
    passwordInput = tk.Entry(loginWindow, show="*")
    passwordInput.pack(pady=5)

    def login():
        username = usernameInput.get()
        password = passwordInput.get()

        c.execute('SELECT password FROM agents WHERE username = ?', (username,))
        saved_Password = c.fetchone()

        if saved_Password and saved_Password[0] == password:
            messagebox.showinfo("Login Successful", "Welcome, Agent!")
            openPropertyWindow()  # Open the property window on successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Button(loginWindow, text="Login", command=login).pack(pady=10)

    def exitApplication():
        conn.close()
        parent_window.destroy()
        loginWindow.destroy()

    tk.Button(loginWindow, text="Exit Application", command=exitApplication).pack(pady=10)

    loginWindow.protocol("WM_DELETE_WINDOW", exitApplication)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Agent Management System")
    root.geometry("400x300")
    root
