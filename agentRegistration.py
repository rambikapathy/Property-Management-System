import tkinter as tk
import sqlite3
import os
import re
import random
import string
import cv2  # OpenCV to capturing images
import webbrowser
from tkinter import Label, Entry, Button, Checkbutton, messagebox, ttk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


# CAPTCHA to help increase security during agent registration
# 'length' is an optional parameter which is defaulted to consist of 6 numbers and characters
def generateCAPTCHA(length=6):
    #Purpose of function
    """Generate a random string of uppercase letters and digits.""" 
    letters_and_digits = string.ascii_uppercase + string.digits
    #'ascii_uppercase' creates a character pool which contains upper case and digits .
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def initiateCaptcha(text, image_size=(200, 60), font_size=36):
    """Create a CAPTCHA image with the given text."""
    # Initiate CAPTCHA
    image = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Textbox size for CAPTCHA
    captchaBox = draw.textbbox((0, 0), text, font=font)
    captchaWidth = captchaBox[2] - captchaBox[0]
    captchaHeight = captchaBox[3] - captchaBox[1]
    captchaTextX = (image_size[0] - captchaWidth) // 2
    captchaTextY = (image_size[1] - captchaHeight) // 2
    draw.text((captchaTextX, captchaTextY), text, font=font, fill=(0, 0, 0))

    # Generate random lines and dots for CAPTCHA image to help increase security
    for _ in range(20):
        x1, y1 = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        x2, y2 = x1 + random.randint(-10, 10), y1 + random.randint(-10, 10)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=1)

    for _ in range(30):
        x, y = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    return image

#Captches and stores agent's face as part of face ID recognition through openCV
def captureAgentFace():
    """Capture agent's face from the webcam and store it to database."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Webcam Error", "Could not open webcam.")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        messagebox.showerror("Capture Error", "Failed to capture image.")
        return None

    #stores image  to faceRecognition database
    image_path = 'captured_face.jpg'
    cv2.imwrite(image_path, frame)
    return image_path

def AgentRegisterWindow(parent_window):
    registrationWindow = tk.Toplevel(parent_window)
    registrationWindow.title("Agent Registration")
    registrationWindow.geometry("450x750")
    registrationWindow.resizable(False, False)  
    registrationWindow.configure(bg="#F5F5DC")  

    # Initiate SQLite database to store agent login/registration credentials.
    conn = sqlite3.connect('agents.db')
    c = conn.cursor()

    # Implement the table for estate agents if it doesn't exist
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

    # Define variables to store agent's inputs in the registration window.
    varName = tk.StringVar()
    varSurname = tk.StringVar()
    varBranch = tk.StringVar()  # This will store the selected branch i.e (Grimsby, Lincoln, etc)
    varEmployeeID = tk.StringVar()
    varUsername = tk.StringVar()  
    varPassword = tk.StringVar()
    varAgree = tk.BooleanVar()
    varCaptcha = tk.StringVar()  # To store CAPTCHA text entered by the user

    # Buttons and entry boxes for agent registration
    tk.Label(registrationWindow, text="Name:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=0, column=0, padx=10, pady=10)
    nameInput = Entry(registrationWindow, textvariable=varName, bg="white", fg="black", width=30)
    nameInput.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Surname:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=1, column=0, padx=10, pady=10)
    surnameInput = Entry(registrationWindow, textvariable=varSurname, bg="white", fg="black", width=30)
    surnameInput.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Branch:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=2, column=0, padx=10, pady=10)
    branchOptions = ["Grimsby", "Lincoln", "Newark", "Gainsborough", "Doncaster", "Scunthorpe"]
    branchInput = ttk.Combobox(registrationWindow, textvariable=varBranch, values=branchOptions, state="readonly", width=27)
    branchInput.grid(row=2, column=1, padx=10, pady=10)
    branchInput.set("Select Branch")  # Placeholder text

    tk.Label(registrationWindow, text="Employee ID:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=3, column=0, padx=10, pady=10)
    employeeIDinput = Entry(registrationWindow, textvariable=varEmployeeID, bg="white", fg="black", width=30)
    employeeIDinput.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Username:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=4, column=0, padx=10, pady=10)
    usernameInput = Entry(registrationWindow, textvariable=varUsername, bg="white", fg="black", width=30)
    usernameInput.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(registrationWindow, text="Password:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=5, column=0, padx=10, pady=10)
    passwordInput = Entry(registrationWindow, textvariable=varPassword, bg="white", fg="black", show="*", width=30)
    passwordInput.grid(row=5, column=1, padx=10, pady=10)

    # Generate CAPTCHA
    captchaText = generateCAPTCHA()
    captchaImage = initiateCaptcha(captchaText)
    captchaImage.save('captcha.png')

    # Display CAPTCHA image in Tkinter window
    captchaPhoto = tk.PhotoImage(file='captcha.png')
    captchaLabel = tk.Label(registrationWindow, image=captchaPhoto, bg="#F5F5DC")
    captchaLabel.image = captchaPhoto  
    captchaLabel.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(registrationWindow, text="Enter CAPTCHA:", width=15, height=1, font=("Open Sans", 12), bg="#F5F5DC", fg="black").grid(row=7, column=0, padx=10, pady=10)
    captchaInput = Entry(registrationWindow, textvariable=varCaptcha, bg="white", fg="black", width=30)
    captchaInput.grid(row=7, column=1, padx=10, pady=10)

    # Users have to validate terms and conditions checkbox
    termsandconditions = Checkbutton(registrationWindow, text="I agree to the terms and conditions", variable=varAgree, bg="#F5F5DC", fg="black", command=lambda: submitButton.config(state="normal" if varAgree.get() else "disabled"))
    termsandconditions.grid(row=8, column=0, columnspan=2, pady=10)

    def GDPRguide():
        filePath = "Guide to GDPR.pdf"  # Adjust path if needed
        if os.path.exists(filePath):
            webbrowser.open(f"file://{os.path.abspath(filePath)}")
        else:
            messagebox.showerror("File Not Found", "GDPR guide not found.")

    pdfLink = tk.Label(registrationWindow, text="Find out about how we process your data under GDPR regulations", font=("Arial", 10), bg="#F5F5DC", fg="black", cursor="hand2")
    pdfLink.grid(row=9, column=0, columnspan=2, pady=10)
    pdfLink.bind("<Button-1>", lambda e: GDPRguide())

    def registrationSubmission():
        nonlocal captchaText, captchaImage, captchaPhoto  # Declare nonlocal variables

        if varAgree.get():
            name = varName.get()
            surname = varSurname.get()
            branchName = varBranch.get()
            employeeID = varEmployeeID.get()
            username = varUsername.get()
            password = varPassword.get()
            captcha = varCaptcha.get()

            # Validate CAPTCHA
            if captcha.upper() != captchaText:
                messagebox.showerror("CAPTCHA Error", "CAPTCHA verification failed. Please try again.")
                # Regenerate new CAPTCHA and update the image
                captchaText = generateCAPTCHA()
                captchaImage = initiateCaptcha(captchaText)
                captchaImage.save('captcha.png')
                captchaPhoto = tk.PhotoImage(file='captcha.png')
                captchaLabel.config(image=captchaPhoto)
                captchaLabel.image = captchaPhoto
                return

            # Validate password complexity. Has to be minimum of 8 characters, 1 number, and 1 symbol.
            if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                messagebox.showerror("Password Requirement", "Password must be at least 8 characters long and contain at least one number and one special symbol.")
                return

            # Capture agent's face and store it into faceRecognition database
            storedAgentFace = captureAgentFace()
            if storedAgentFace:
                # Store image in faceRecognition database
                faceConn = sqlite3.connect('faceRecognition.db')
                faceCursor = faceConn.cursor()
                faceCursor.execute('''CREATE TABLE IF NOT EXISTS agent_faces (
                                        username TEXT PRIMARY KEY,
                                        image_path TEXT NOT NULL
                                    )''')
                faceCursor.execute('INSERT INTO agent_faces (username, image_path) VALUES (?, ?)', (username, storedAgentFace))
                faceConn.commit()
                faceConn.close()
            
            try:
                # Insert agent's input into the database if unique constraints are met
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
                varCaptcha.set("")
                
                # Close the registration window
                registrationWindow.destroy()
                
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    messagebox.showerror("Registration Failed", "Employee ID or Username already exists.")
        else:
            messagebox.showwarning("Agreement Required", "You must agree to the terms and conditions to register.")

    # Disable the submit button if terms & conditions are not checked
    submitButton = Button(registrationWindow, text="Submit Registration", state="disabled", command=registrationSubmission, bg="#8B4513", fg="white")  # Brown button
    submitButton.grid(row=10, column=0, columnspan=2, pady=20)

    # Exit button to close the registration window
    exitButton = Button(registrationWindow, text="Exit", command=registrationWindow.destroy, bg="#8B4513", fg="white")  # Brown button
    exitButton.grid(row=11, column=0, columnspan=2, pady=10)

    registrationWindow.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rishi's Property Management System")
    root.geometry("400x300")
    root.configure(bg="black")

    # Start the agent registration window
    AgentRegisterWindow(root)
