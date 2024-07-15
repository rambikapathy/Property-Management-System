import tkinter as tk
import os
from tkinter import Label, Entry, Button, messagebox
import webbrowser

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
    varAgree = tk.BooleanVar()

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

    # Users have to validate terms and conditions checkbox
    termsandconditions = tk.Checkbutton(registrationWindow, text="I agree to the terms and conditions", variable=varAgree, bg="blue", fg="white", command=lambda: submitButton.config(state="normal" if varAgree.get() else "disabled"))
    termsandconditions.grid(row=6, column=0, columnspan=2, pady=10)

    # Guide to GDPR for users who wish to find how my system stores and processed data 
    def GDPRguide():
        filePath = "/Users/nikhishaambi/Desktop/Research Project/Guide to GDPR.pdf"
        if os.path.exists(filePath):
            webbrowser.open(f"file://{filePath}")
        else:
            messagebox.showerror("File Not Found")

    pdfLink = tk.Label(registrationWindow, text="Find out about how we process your data under GDPR  regulations", font=("Arial", 10), bg="blue", fg="white", cursor="hand2")
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
        else:
            messagebox.showwarning("Agreement Required", "You must agree to the terms and conditions to register.")

    # Disable the submit button if terms & conditions are not checked by the agent whilst registering.
    submitButton = tk.Button(registrationWindow, text="Submit Registration", state="disabled", command=registrationSubmission)
    submitButton.grid(row=8, column=0, columnspan=2, pady=20)
