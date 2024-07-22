import tkinter as tk
from tkinter import messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk
import random
import string
from propertyWindow import openPropertyWindow
import os

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

def intiateOTPcode(length=6):
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=length))

def AgentLoginWindow(parent_window):
    loginWindow = tk.Toplevel(parent_window, bg="black")
    loginWindow.title("Agent Login")
    loginWindow.geometry("400x625")
    loginWindow.resizable(False, False)

    conn = sqlite3.connect('agents.db')
    c = conn.cursor()

    # Generate a 6-digit OTP for each session
    otp = intiateOTPcode()  
    qrCodeImage = "qrcode.png"
    initiateQRCode(otp, qrCodeImage)

    # Load QR code 
    qrImage = Image.open(qrCodeImage)
    qrPhoto = ImageTk.PhotoImage(qrImage)

    tk.Label(loginWindow, text="Username:", bg="black", fg="white").pack(pady=10)
    usernameInput = tk.Entry(loginWindow)
    usernameInput.pack(pady=5)

    tk.Label(loginWindow, text="Password:", bg="black", fg="white").pack(pady=10)
    passwordInput = tk.Entry(loginWindow, show="*")
    passwordInput.pack(pady=5)

    # Display QR code image
    qrCode = tk.Label(loginWindow, image=qrPhoto, bg="black")
    qrCode.photo = qrPhoto  # Keep a reference to avoid garbage collection
    qrCode.pack(pady=10)

    tk.Label(loginWindow, text="Please enter QR code:", bg="black", fg="white").pack(pady=10)
    otpInput = tk.Entry(loginWindow)
    otpInput.pack(pady=5)

    def login():
        username = usernameInput.get()
        password = passwordInput.get()
        OTP = otpInput.get()

        # Validate OTP
        if OTP != otp:
            messagebox.showerror("OTP Error", "Invalid OTP. Please try again.")
            return

        c.execute('SELECT password FROM agents WHERE username = ?', (username,))
        saved_Password = c.fetchone()

        if saved_Password and saved_Password[0] == password:
            messagebox.showinfo("Login Successful", "Welcome, Agent!")
            openPropertyWindow()  # Open the property window on successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Button(loginWindow, text="Login", command=login).pack(pady=10)

    def closeWindow():
        conn.close()
        os.remove(qrCodeImage)  # Clean up the QR code file at the end of each login session
        loginWindow.destroy()

    tk.Button(loginWindow, text="Close Window", command=closeWindow).pack(pady=10)

    loginWindow.protocol("WM_DELETE_WINDOW", closeWindow)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rishi's Property Management System")
    root.geometry("400x300")
    root.configure(bg="black")
    tk.Button(root, text="Agent Login", command=lambda: AgentLoginWindow(root)).pack(pady=20)
    root.mainloop()
