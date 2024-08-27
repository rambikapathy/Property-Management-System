import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
from faceRecognition import validateAgentFaceID, retrieveFaceID
from propertyWindow import openPropertyWindow
from diaryWindow import optimiseDiaryWindow
from chatbotWindow import optimiseFAQ_ChatbotWindow
from systemLogWindow import systemLogWindow

def MainMenuWindow(parent_window):
    # Close the parent window (e.g., login window), if login is sucessful. this keeps the program as compact and efficient as possible
    parent_window.destroy()

    # Implement another root window called 'main menu' to help bring all the functionalities of the system into one place.
    mainMenuWindow = tk.Toplevel()
    mainMenuWindow.title("Rishi's Property Management System - Main Menu")
    mainMenuWindow.geometry("800x700")
    mainMenuWindow.config(bg="#F5F5DC")  
    mainMenuWindow.resizable(False, False)  

    tk.Label(mainMenuWindow, text="Main Menu", font=("Helvetica", 16), bg="#F5F5DC").pack(pady=10)

    # Function to access diary window, note that this is subject to succesfull Face ID recognition.
    def optimiseAppointment():
        registered_faces = retrieveFaceID()
        if validateAgentFaceID(registered_faces):
            optimiseDiaryWindow()
        else:
            messagebox.showerror("Authentication Failed", "Face not recognized. Access denied.")

    # Function to access 'active system monitoring' window, note that this is subject to succesfull Face ID recognition.
    def optimiseSystemLog():
        registered_faces = retrieveFaceID()
        if validateAgentFaceID(registered_faces):
            systemLogWindow(mainMenuWindow)
        else:
            messagebox.showerror("Authentication Failed", "Face not recognized. Access denied.")

    # Improved buttons/widgets with meaningful icons for each functionalities. This is to help improve user experience, making desing more versatile.
    appointmentDiaryIcon = ImageTk.PhotoImage(Image.open("diary.png").resize((50, 50))) # button for booking appointment
    closeIcon = ImageTk.PhotoImage(Image.open("close.png").resize((50, 50))) # close window
    systemLogIcon = ImageTk.PhotoImage(Image.open("log.png").resize((50, 50))) #active system monitoring
    faqChatbotIcon = ImageTk.PhotoImage(Image.open("faq.png").resize((50, 50))) # FAQ chatbot
    propertyIcon = ImageTk.PhotoImage(Image.open("property.png").resize((50, 50))) # Property lisiting, including the adding, deletion of properties.

    #Buttons that optimise core application functionalities
    tk.Button(mainMenuWindow, image=appointmentDiaryIcon, command=optimiseAppointment, bg="#F5F5DC").pack(pady=5)
    tk.Button(mainMenuWindow, image=propertyIcon, command=openPropertyWindow, bg="#F5F5DC").pack(pady=5)
    tk.Button(mainMenuWindow, image=faqChatbotIcon, command=optimiseFAQ_ChatbotWindow, bg="#F5F5DC").pack(pady=5)
    tk.Button(mainMenuWindow, image=systemLogIcon, command=optimiseSystemLog, bg="#F5F5DC").pack(pady=5)
    tk.Button(mainMenuWindow, image=closeIcon, command=mainMenuWindow.destroy, bg="#F5F5DC").pack(pady=10)

    # Reference to image icons for buttons
    mainMenuWindow.dl_icon = appointmentDiaryIcon
    mainMenuWindow.cl_icon = closeIcon
    mainMenuWindow.sl_icon = systemLogIcon
    mainMenuWindow.fq_icon = faqChatbotIcon
    mainMenuWindow.pr_icon = propertyIcon

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rishi's Property Management System")
    root.geometry("400x300")
    root.config(bg="#F5F5DC")  
    root.withdraw()  

    MainMenuWindow(root)
    root.mainloop()
