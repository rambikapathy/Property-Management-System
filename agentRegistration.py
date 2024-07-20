import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, ttk
import sqlite3
import os
import re
from datetime import datetime
import webbrowser

def AgentRegisterWindow(parent_window):
    registrationWindow = tk.Toplevel(parent_window, bg="black")
    registrationWindow.title("Agent Registration")
    registrationWindow.geometry("450x650")  
    registrationWindow.resizable(False, False)  # Resizing disabled
    
    # Initiate SQLite database to store agent login/registration credentials.
    conn = sqlite3.connect('agents.db')
    c = conn.cursor()

    # Implement the table for estate agents table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS agents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    branch TEXT NOT NULL,
                    employee_id TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    registration_date TEXT NOT NULL
                )''')
    conn.commit()

    # Define variables to store agent's inputs in registration window.
    varName = tk.StringVar()
    varSurname = tk.StringVar()
    varBranch = tk.StringVar()  # This will store the selected branch
    varEmployeeID = tk.StringVar()
    varUsername = tk.StringVar()
    varPassword = tk.StringVar()
    varAgree = tk.BooleanVar()

    tk.Label(registrationWindow, text="Name:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10)
    nameInput = Entry(registrationWindow, textvariable=varName, bg="white", fg="black", width=30)
    nameInput.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Surname:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10)
    surnameInput = Entry(registrationWindow, textvariable=varSurname, bg="white", fg="black", width=30)
    surnameInput.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Branch:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=2, column=0, padx=10, pady=10)
    branchOptions = ["Grimsby", "Lincoln", "Newark", "Gainsborough", "Doncaster", "Scunthorpe"]
    branchInput = ttk.Combobox(registrationWindow, textvariable=varBranch, values=branchOptions, state="readonly", width=27)
    branchInput.grid(row=2, column=1, padx=10, pady=10)
    branchInput.set("Select Branch")  # Placeholder text

    tk.Label(registrationWindow, text="Employee ID:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=3, column=0, padx=10, pady=10)
    employeeIDinput = Entry(registrationWindow, textvariable=varEmployeeID, bg="white", fg="black", width=30)
    employeeIDinput.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Username:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=4, column=0, padx=10, pady=10)
    usernameInput = Entry(registrationWindow, textvariable=varUsername, bg="white", fg="black", width=30)
    usernameInput.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Password:", width=15, height=1, font=("Open Sans", 12), bg="black", fg="white").grid(row=5, column=0, padx=10, pady=10)
    passwordInput = Entry(registrationWindow, textvariable=varPassword, bg="white", fg="black", show="*", width=30)
    passwordInput.grid(row=5, column=1, padx=10, pady=10)

    # Users have to validate terms and conditions checkbox
    termsandconditions = tk.Checkbutton(registrationWindow, text="I agree to the terms and conditions", variable=varAgree, bg="black", fg="white", command=lambda: submitButton.config(state="normal" if varAgree.get() else "disabled"))
    termsandconditions.grid(row=6, column=0, columnspan=2, pady=10)

    # Guide to GDPR for users who wish to find how my system stores and processes data
    def GDPRguide():
        filePath = "Guide to GDPR.pdf"  # Adjust path if needed
        if os.path.exists(filePath):
            webbrowser.open(f"file://{os.path.abspath(filePath)}")
        else:
            messagebox.showerror("File Not Found", "GDPR guide not found.")

    pdfLink = tk.Label(registrationWindow, text="Find out about how we process your data under GDPR regulations", font=("Arial", 10), bg="black", fg="white", cursor="hand2")
    pdfLink.grid(row=7, column=0, columnspan=2, pady=10)
    pdfLink.bind("<Button-1>", lambda e: GDPRguide())
    
    def registrationSubmission():
        if varAgree.get():
            name = varName.get()
            surname = varSurname.get()
            branchName = varBranch.get()
            employeeID = varEmployeeID.get()
            username = varUsername.get()
            password = varPassword.get()
            
            # Validate password complexity. Has to be minimum of 8 characters, 1 number and 1 symbol.
            if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                messagebox.showerror("Password Requirement", "Password must be at least 8 characters long and contain at least one number and one special symbol.")
                return
            
            try:
                # Insert agent's input into database if unique constraints are met
                c.execute('''INSERT INTO agents (name, surname, branch, employee_id, username, password, registration_date)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (name, surname, branchName, employeeID, username, password, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                
                messagebox.showinfo("Registration", f"Registered:\nName: {name}\nSurname: {surname}\nBranch: {branchName}\nEmployee ID: {employeeID}\nUsername: {username}")
                
                # Clear the entries after submission
                varName.set("")
                varSurname.set("")
                varBranch.set("Select Branch")
                varEmployeeID.set("")
                varUsername.set("")
                varPassword.set("")
                
                # Close the registration window
                registrationWindow.destroy()
                
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    messagebox.showerror("Registration Failed", "Employee ID or Username already exists.")
        else:
            messagebox.showwarning("Agreement Required", "You must agree to the terms and conditions to register.")

    # Disable the submit button if terms & conditions are not checked
    submitButton = tk.Button(registrationWindow, text="Submit Registration", state="disabled", command=registrationSubmission)
    submitButton.grid(row=8, column=0, columnspan=2, pady=20)

    # Exit button to close the registration window
    exitButton = tk.Button(registrationWindow, text="Exit", command=registrationWindow.destroy)
    exitButton.grid(row=9, column=0, columnspan=2, pady=10)

    registrationWindow.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Agent Management System")
    root.geometry("400x300")
    root.configure(bg="black")

    # Start the agent registration window
    AgentRegisterWindow(root)
