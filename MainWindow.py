##import necessary libraries
import tkinter as tk
from tkVideoPlayer import TkinterVideo #allows video to be played on main screen to help enhance the GUI design.
from agentRegistration import AgentRegisterWindow #import code files
from agentLogin import AgentLoginWindow

def mainWindow():
    global window
    window = tk.Tk()
    window.geometry("800x700")
    window.title("Rishi's Property Management System")
    window.configure(bg="#F5F5DC")  

    def windowButtons(parent, text, command):
        buttonFrame = tk.Frame(parent, bg="#D2B48C")
        buttonFrame.pack(side="left", padx=30)
        buttonSize = 120  
        buttonWidth = buttonSize + 20  
        circularButton = tk.Canvas(buttonFrame, width=buttonWidth, height=buttonWidth, bg="#F5F5DC", highlightthickness=0)
        circularButton.create_oval(10, 10, buttonSize, buttonSize, fill="#D2B48C", outline="#D2B48895C") 
        circularButton.pack() 

        ## Adjust font size and button dimensions, so that it fits within the framework.
        buttonFontSize = 12  
        button = tk.Button(buttonFrame, text=text, command=command, fg="black", bg="#D2B48C", relief="flat",
                           font=("Arial", buttonFontSize), width=8, height=2, padx=0, pady=0)
        button.place(relx=0.5, rely=0.5, anchor="center")

    # Iniaite video player to help elevate GUI design.
    # Implement frame for video player using tkVideoPlayer to enhance system design and to make GUI more appeasing
    videoPlayerFrame = tk.Frame(window, width=800, height=550, bg="#F5F5DC")
    videoPlayerFrame.pack(expand=True, fill="both")
    mainWindowVideo = TkinterVideo(videoPlayerFrame, scaled=True)
    mainWindowVideo.load(r"mainVideo.mp4")
    mainWindowVideo.pack(expand=True, fill="both")
    mainWindowVideo.play()

    buttonsFrame = tk.Frame(window, bg="#F5F5DC")
    buttonsFrame.pack(side="top", pady=20)

    windowButtons(buttonsFrame, "Login", lambda: AgentLoginWindow(window))
    windowButtons(buttonsFrame, "Registration", lambda: AgentRegisterWindow(window))
    windowButtons(buttonsFrame, "Exit", window.destroy)
    
    window.mainloop()

if __name__ == "__main__":
    mainWindow()


