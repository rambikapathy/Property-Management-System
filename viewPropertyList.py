import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

# Initialize connection to database
def createConnection():
    conn = sqlite3.connect('properties.db')
    return conn

def viewPropertyListWindow():
    viewWindow = tk.Toplevel(bg="black")
    viewWindow.title("View Properties")
    viewWindow.geometry("800x600")
    viewWindow.resizable(False, False)

    tk.Label(viewWindow, text="Properties List", bg="black", fg="white").pack(pady=20)

    frame = tk.Frame(viewWindow, bg="black")
    frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame, bg="black")
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollableFrame = tk.Frame(canvas, bg="black")

    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM properties")
    properties = c.fetchall()
    conn.close()
    
    for prop in properties:
        photoFrame = tk.Frame(scrollableFrame, bg="black", pady=5)
        photoFrame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(photoFrame, text=f"ID: {prop[0]}", bg="black", fg="white").grid(row=0, column=0, sticky="w")
        tk.Label(photoFrame, text=f"Address: {prop[1]}", bg="black", fg="white").grid(row=0, column=1, sticky="w")
        tk.Label(photoFrame, text=f"Price: £{prop[2]}", bg="black", fg="white").grid(row=0, column=2, sticky="w")
        tk.Label(photoFrame, text=f"Bedrooms: {prop[3]}", bg="black", fg="white").grid(row=0, column=3, sticky="w")
        tk.Label(photoFrame, text=f"Category: {prop[4]}", bg="black", fg="white").grid(row=1, column=0, sticky="w")
        tk.Label(photoFrame, text=f"Market Date: {prop[5]}", bg="black", fg="white").grid(row=1, column=1, sticky="w")
        tk.Label(photoFrame, text=f"Vendor: {prop[6]}", bg="black", fg="white").grid(row=1, column=2, sticky="w")
        
        propertyPhoto = prop[7]
        if propertyPhoto and propertyPhoto != "":
            try:
                img = Image.open(propertyPhoto)
                img = img.resize((150, 150), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                panel = tk.Label(photoFrame, image=img, bg="black")
                panel.image = img  # Keep a reference to avoid garbage collection
                panel.grid(row=0, column=4, rowspan=2, padx=10, pady=5)
            except Exception as e:
                tk.Label(photoFrame, text="Photo not available", bg="black", fg="white").grid(row=0, column=4, rowspan=2, padx=10, pady=5)

    tk.Button(viewWindow, text="Close Window", command=viewWindow.destroy).pack(pady=10)

# Main Execution Block
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rishi's Property Management System")
    root.geometry("400x300")
    root.configure(bg="black")

    tk.Button(root, text="View Property List", command=viewPropertyListWindow).pack(pady=20)

    root.mainloop()
