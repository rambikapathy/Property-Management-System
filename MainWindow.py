import tkinter as tk
import time
from agentRegistration import AgentRegisterWindow
from agentLogin import AgentLoginWindow

def main_window():
    global window
    window = tk.Tk()
    window.geometry("400x300")
    window.title("Rishi's Property Management System")
    window.configure(bg="blue")
    
    # Function to update the time label
    def update_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        time_label.config(text=f"Current Date & Time: {current_time}")
        window.after(1000, update_time)  # Update every second
    
    # Label and display current date and time on application
    time_label = tk.Label(window, text="", font=("Arial", 12), bg="blue", fg="white")
    time_label.pack(pady=10)
    
    # Start updating the time label each second
    update_time()

    tk.Label(window, text="", bg="blue").pack()
    tk.Button(window, text="Agent Login", width=20, height=2, command=lambda: AgentLoginWindow(window)).pack(pady=10)
    tk.Button(window, text="Agent Registration", width=20, height=2, command=lambda: AgentRegisterWindow(window)).pack(pady=10)
    
    # Exit button to close the application
    tk.Button(window, text="Exit", width=20, height=2, command=window.destroy).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main_window()
