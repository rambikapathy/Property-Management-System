import tkinter as tk
from tkinter import messagebox
import sqlite3
import qrcode
import random
import string
import os
from PIL import Image, ImageTk
from bcrypt import hashpw, gensalt
from mainMenu import MainMenuWindow  
from agentRegistration import AgentRegisterWindow

#iniate QR code PNG.
def initiateQRCode(data, filename="qrcode.png"): 
    """Generate a QR code image with the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def initiateOTPcode(length=6):
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=length))

#Open login window
def AgentLoginWindow(parent_window):
    def closeWindow():
        if os.path.exists(qrCodeImage):
            os.remove(qrCodeImage)  
            # Clean up and regenerate QR code file at the end of each login session
        conn.close()
        loginWindow.destroy()
        # Reopen the parent window
        parent_window.deiconify()  
    
    #Link to Registration Window.
    def openRegistrationWindow():
        loginWindow.withdraw()  
        # Hide the login window if registration windown is open.
        AgentRegisterWindow(loginWindow)  
        # Open the registration window

# Hide the parent window (Main Window.py)
    parent_window.withdraw()  

    loginWindow = tk.Toplevel(parent_window)
    loginWindow.title("Agent Login")
    loginWindow.geometry("400x725")
    loginWindow.resizable(False, False)
    loginWindow.configure(bg="#F5F5DC")  

    #connect to database
    conn = sqlite3.connect('agents.db')
    c = conn.cursor()

    # Generate a unique 6-digit OTP for each session
    otp = initiateOTPcode()
    qrCodeImage = "qrcode.png"
    initiateQRCode(otp, qrCodeImage)

    # Load QR code
    qrImage = Image.open(qrCodeImage)
    qrPhoto = ImageTk.PhotoImage(qrImage)

    #Take in user login input
    tk.Label(loginWindow, text="Username:", bg="#F5F5DC", fg="black").pack(pady=10)
    usernameInput = tk.Entry(loginWindow)
    usernameInput.pack(pady=5)

    tk.Label(loginWindow, text="Password:", bg="#F5F5DC", fg="black").pack(pady=10)
    passwordInput = tk.Entry(loginWindow, show="*")
    passwordInput.pack(pady=5)

    # Display QR code image
    qrCode = tk.Label(loginWindow, image=qrPhoto, bg="#F5F5DC")
    qrCode.photo = qrPhoto  # Keep a reference to avoid garbage collection
    qrCode.pack(pady=10)

    #Ask user to input OTP code seen whilst scanning QR code.
    tk.Label(loginWindow, text="Please enter QR code:", bg="#F5F5DC", fg="black").pack(pady=10)
    otpInput = tk.Entry(loginWindow)
    otpInput.pack(pady=5)

    def login():
        username = usernameInput.get()
        password = passwordInput.get()
        OTP = otpInput.get()

        # Validate OTP, if incorrect output error.
        if OTP != otp:
            messagebox.showerror("OTP Error", "Invalid OTP. Please try again.")
            return

        c.execute('SELECT password FROM agents WHERE username = ?', (username,))
        storedPassword = c.fetchone()
    # Open the MainMenu window on successful login
        if storedPassword and storedPassword[0] == password:
            messagebox.showinfo("Login Successful", "Welcome, Agent!")
            MainMenuWindow(loginWindow) 
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    #Buttons
    tk.Button(loginWindow, text="Login", command=login, bg="#8B4513", fg="white").pack(pady=10)
    tk.Button(loginWindow, text="Register", command=openRegistrationWindow, bg="#8B4513", fg="white").pack(pady=10)
    tk.Button(loginWindow, text="Close Window", command=closeWindow, bg="#8B4513", fg="white").pack(pady=10)

    loginWindow.protocol("WM_DELETE_WINDOW", closeWindow)

# Function to allow user to go back to Main Window.py page if they decided to exit login window.
def createMainWindow():
    mainWindow = tk.Tk()
    mainWindow.title("Main Window")
    mainWindow.geometry("400x300")
    mainWindow.configure(bg="#F5F5DC")  
    tk.Button(mainWindow, text="Open Agent Login", command=lambda: AgentLoginWindow(mainWindow), bg="#8B4513", fg="white").pack(pady=20)

    mainWindow.mainloop()

if __name__ == "__main__":
    createMainWindow()


