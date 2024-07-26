import tkinter as tk
from tkinter import ttk
import time
from tkVideoPlayer import TkinterVideo
from agentRegistration import AgentRegisterWindow
from agentLogin import AgentLoginWindow

def mainWindow():
    global window
    window = tk.Tk()
    window.geometry("800x700")
    window.title("Rishi's Property Management System")
    window.configure(bg="#B0E0E6")
    
    def updateTime():
        currentTime = time.strftime('%d-%m-%Y %H:%M:%S')
        displayTime.config(text=f" {currentTime}", font=("Gill Sans", 25))
        window.after(1000, updateTime)  # Update every second
    
    # Display current date and time
    displayTime = tk.Label(window, text="", font=("Arial", 12), bg="#B0E0E6", fg="black")
    displayTime.pack(pady=10)
    
    # Update time each second
    updateTime()
    
    def buttons(canvas, x, y, radius, text, command):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")
        button = tk.Button(window, text=text, command=command, fg="white", bg="black", relief="flat")
        button_window = canvas.create_window(x, y, window=button)
        return button_window
    
    # Canvas has been created to initiate circular buttons that help elevate design of the system to make it look more pleasing
    canvas = tk.Canvas(window, width=400, height=300, bg="#B0E0E6", highlightthickness=0)
    canvas.pack(pady=10)
    
    # Create circular buttons
    buttons(canvas, 200, 50, 40, "Login", lambda: AgentLoginWindow(window))
    buttons(canvas, 200, 130, 40, "Registration", lambda: AgentRegisterWindow(window))
    
    # Exit button
    buttons(canvas, 200, 210, 40, "Exit", window.destroy)
    
    # Create a frame for the video player to enhance design aspects of system
    videoPlayerFrame = tk.Frame(window, width=800, height=700)
    videoPlayerFrame.pack(expand=True, fill="both")
    videoPlayerFrame.pack_propagate(False)
    
    # Video player using tkVideoPlayer
    mainWindowVideo = TkinterVideo(videoPlayerFrame, scaled=True)
    mainWindowVideo.load(r"mainVideo.mp4")
    mainWindowVideo.pack(expand=True, fill="both")
    mainWindowVideo.play()
    
    window.mainloop()

if __name__ == "__main__":
    mainWindow()
