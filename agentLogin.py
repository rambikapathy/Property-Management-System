import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

def AgentLoginWindow(parent_window):
    loginWindow = tk.Toplevel(parent_window, bg="black")
    loginWindow.title("Agent Login")
    loginWindow.geometry("400x250")  # Increased size
    loginWindow.resizable(False, False)  # Disable resizing
    
    # Hide password whilst and after user input.
    def hidePassword(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Connect to SQLite database
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
        
        # Retrieve hashed password from database
        c.execute('SELECT password FROM agents WHERE username = ?', (username,))
        saved_Password = c.fetchone()
        
        if saved_Password:
            saved_Password = saved_Password[0]
            hidden_Password = hidePassword(password)
            
            if hidden_Password == saved_Password:
                messagebox.showinfo("Login Successful", "Welcome, Agent!")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    tk.Button(loginWindow, text="Login", command=login).pack(pady=10)
    
    # Exit button to close the application
    def exitApplication():
        conn.close()  # Close database connection
        parent_window.destroy()  # Close the main window
        loginWindow.destroy()  # Close the login window

    exitButton = tk.Button(loginWindow, text="Exit Application", command=exitApplication)
    exitButton.pack(pady=10)

    # Close database connection when window is closed
    loginWindow.protocol("WM_DELETE_WINDOW", exitApplication)

    loginWindow.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Agent Management System")
    root.geometry("400x300")
    root.configure(bg="black")

    # Start the agent login window
    AgentLoginWindow(root)
