import tkinter as tk
import time
from agentRegistration import AgentRegisterWindow
from agentLogin import AgentLoginWindow

def main_window():
    global window
    window = tk.Tk()
    window.geometry("400x300")
    window.title("Rishi's Property Management System")
    window.configure(bg="black")
    
    # Function to update the time label
    def updateTime():
        currentTime = time.strftime('%d-%m-%Y %H:%M:%S')
        displayTime.config(text=f" {currentTime}",font=("Comic Sans", 25))
        window.after(1000, updateTime)  # Update every second
    
    # Label and display current date and time on application
    displayTime = tk.Label(window, text="", font=("Arial", 12), bg="black", fg="white")
    displayTime.pack(pady=10)
    
    # Start updating the time label each second
    updateTime()

    tk.Label(window, text="", bg="black").pack()
    tk.Button(window, text="Agent Login", width=20, height=2, command=lambda: AgentLoginWindow(window)).pack(pady=10)
    tk.Button(window, text="Agent Registration", width=20, height=2, command=lambda: AgentRegisterWindow(window)).pack(pady=10)
    
    # Exit button to close the application
    tk.Button(window, text="Exit", width=20, height=2, command=window.destroy).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main_window()
