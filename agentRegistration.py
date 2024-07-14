import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

def AgentRegisterWindow(parent_window):
    registrationWindow = tk.Toplevel(parent_window, bg="blue")
    registrationWindow.title("Agent Registration")
    registrationWindow.geometry("400x400")
    
    # Define variables to store agent's inputs in registration window.
    varName = tk.StringVar()
    varSurname = tk.StringVar()
    varBranch = tk.StringVar()
    varEmployeeID = tk.StringVar()
    varUsername = tk.StringVar()
    varPassword = tk.StringVar()

    tk.Label(registrationWindow, text="Name:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=0, column=0, padx=10, pady=10)
    nameInput = Entry(registrationWindow, textvariable=varName, bg="white", width=30)
    nameInput.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Surname:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=1, column=0, padx=10, pady=10)
    surnameInput = Entry(registrationWindow, textvariable=varSurname, bg="white", width=30)
    surnameInput.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Branch:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=2, column=0, padx=10, pady=10)
    branchInput = Entry(registrationWindow, textvariable=varBranch, bg="white", width=30)
    branchInput.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Employee ID:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=3, column=0, padx=10, pady=10)
    employeeIDinput = Entry(registrationWindow, textvariable=varEmployeeID, bg="white", width=30)
    employeeIDinput.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Username:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=4, column=0, padx=10, pady=10)
    usernameInput = Entry(registrationWindow, textvariable=varUsername, bg="white", width=30)
    usernameInput.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Password:", width=15, height=1, font=("Times New Roman", 12), bg="blue", fg="white").grid(row=5, column=0, padx=10, pady=10)
    passwordInput = Entry(registrationWindow, textvariable=varPassword, bg="white", show="*", width=30)
    passwordInput.grid(row=5, column=1, padx=10, pady=10)

    def registrationSubmission():
        name = varName.get()
        surname = varSurname.get()
        branchName = varBranch.get()
        employeeID = varEmployeeID.get()
        username = varUsername.get()
        password = varPassword.get()
        
        # Example of using the data (you can replace with your database code)
        messagebox.showinfo("Registration", f"Registered:\nName: {name}\nSurname: {surname}\nBranch: {branchName}\nEmployee ID: {employeeID}\nUsername: {username}\nPassword: {password}")
        
        # Clear the entries after submission
        varName.set("")
        varSurname.set("")
        varBranch.set("")
        varEmployeeID.set("")
        varUsername.set("")
        varPassword.set("")
        
        # Close the registration window
        registrationWindow.destroy()
        
        # Open the login window
        from agentLogin import AgentLoginWindow
        AgentLoginWindow(parent_window)

    tk.Button(registrationWindow, text="Submit Registration", command=registrationSubmission).grid(row=6, column=0, columnspan=2, pady=20)
