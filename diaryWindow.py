import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk
import datetime
import re
import sqlite3
from appointments import filterAppointments, initiateAppointment, deleteAppointment

#retrieves property data from database through executing query
def searchProperties():
    """Fetch properties from the properties database."""
    conn = sqlite3.connect('properties.db')
    cursor = conn.cursor() # cursor is iniated to allow interaction between database
    cursor.execute("SELECT id, address FROM properties")
    properties = cursor.fetchall()
    conn.close()
    return properties

#function to retreive property address from database
def retreivePropertyAddress(property_id):
    """Fetch the address of a property given its ID."""
    conn = sqlite3.connect('properties.db')
    cursor = conn.cursor()
    cursor.execute("SELECT address FROM properties WHERE id=?", (property_id,))
    #retreive the first set of results if the query exists.
    address = cursor.fetchone()
    conn.close()
    #if address is not retreived, throw error to the agent stating unknown address.
    return address[0] if address else "Unknown Property"

#ensure contact number is 11 digits
def validateContactNumber(number):
    """Check if the contact number is valid (11 digits)."""
    return re.fullmatch(r'\d{11}', number) is not None

def validateAppointmentTime(time):
    """Check if the appointment time is within the allowed range."""
    return datetime.time(9, 0) <= time <= datetime.time(15, 0)

#Initiate window for appointments/diary
def optimiseDiaryWindow():
    appointmentDiary = tk.Toplevel()
    appointmentDiary.title("Diary")
    appointmentDiary.geometry("1200x800")
    appointmentDiary.configure(bg="beige")
    appointmentDiary.resizable(True, True)

    tk.Label(appointmentDiary, text="Appointments Diary", bg="beige", fg="black", font=("Arial", 18)).grid(row=0, column=0, columnspan=3, pady=10, padx=10)
#Augment framework to structure the contents inside Diary window
    frame = tk.Frame(appointmentDiary, bg="beige")
    frame.grid(row=1, column=0, sticky='nsew')
#Split the frame left to take input fron agent to confirm and store bookings
    frameL = tk.Frame(frame, bg="beige")
    frameL.grid(row=0, column=0, sticky='nsew')
#Splite the frame right to output confirmed appointments to user in a treeview format.
    frameR = tk.Frame(frame, bg="beige")
    frameR.grid(row=0, column=1, sticky='nsew')
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)

#Add calendar on the left hand side of the frame
    cal = Calendar(frameL, selectmode='day', date_pattern='yyyy-mm-dd',
                   background='beige', foreground='black', headersbackground='grey',
                   normalbackground='beige', normalforeground='black',
                   selectbackground='blue', selectforeground='black')
    cal.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')

    dateTag = tk.Label(frameL, text="Select Date:", bg="beige", fg="black")
    dateTag.grid(row=1, column=0, pady=5)

    dateVariable = tk.StringVar()
    dateSelection = ttk.Combobox(frameL, textvariable=dateVariable)
    dateSelection.grid(row=2, column=0, pady=5, sticky='ew')

    timeTag = tk.Label(frameL, text="Select Time Slot:", bg="beige", fg="black")
    timeTag.grid(row=3, column=0, pady=5)
    #Dropdown bar for date and time selection
    timeVariable = tk.StringVar()
    timeMenu = ttk.Combobox(frameL, textvariable=timeVariable)
    appointmentSlots = [f"{hour:02d}:{minute:02d}" for hour in range(9, 15) for minute in [0, 30]]
    timeMenu['values'] = appointmentSlots
    timeMenu.grid(row=4, column=0, pady=5, sticky='ew')
#Retreive currently available property from property database for agent to book appointment with viewer.
    propertyIdentifier = tk.Label(frameL, text="Select Property:", bg="beige", fg="black")
    propertyIdentifier.grid(row=5, column=0, pady=5)

    propertyVariable = tk.StringVar()
    propertyMenu = ttk.Combobox(frameL, textvariable=propertyVariable, state="readonly")
    propertyMenu.grid(row=6, column=0, pady=5, sticky='ew')

    tk.Label(frameL, text="Viewer Name:", bg="beige", fg="black").grid(row=7, column=0, pady=5)
    inputViewerName = tk.Entry(frameL, width=40)
    inputViewerName.grid(row=8, column=0, pady=5, sticky='ew')

    tk.Label(frameL, text="Contact Number (11 digits):", bg="beige", fg="black").grid(row=9, column=0, pady=5)
    inputViewerContactNumber = tk.Entry(frameL, width=40)
    inputViewerContactNumber.grid(row=10, column=0, pady=5, sticky='ew')

    tk.Label(frameL, text="Email Address:", bg="beige", fg="black").grid(row=11, column=0, pady=5)
    emailInput = tk.Entry(frameL, width=40)
    emailInput.grid(row=12, column=0, pady=5, sticky='ew')

#Add appointment notes
    notes = tk.Label(frameL, text="Notes:", bg="beige", fg="black")
    notes.grid(row=13, column=0, pady=5)
    appointmentText = tk.Text(frameL, wrap=tk.WORD, height=5, bg="beige", fg="black")
    appointmentText.grid(row=14, column=0, pady=10, padx=10, sticky='nsew')
#Output the confirmed viewing appointments on the right hand side of the framework, outputting relevant appointment details, such as viewer name, property address, viewing date/time etc.
    confirmedAppointments = ttk.Treeview(frameR, columns=("ID", "Date", "Property", "Time", "Viewer Name", "Contact Number", "Email Address", "Notes"), show='headings')
    
#Headings for Appointment treeview 
    confirmedAppointments.heading("ID", text="ID")
    confirmedAppointments.heading("Date", text="Date")
    confirmedAppointments.heading("Property", text="Property")
    confirmedAppointments.heading("Time", text="Time")
    confirmedAppointments.heading("Viewer Name", text="Viewer Name")
    confirmedAppointments.heading("Contact Number", text="Contact Number")
    confirmedAppointments.heading("Email Address", text="Email Address")
    confirmedAppointments.heading("Notes", text="Notes")
    confirmedAppointments.column("ID", width=30)             
    confirmedAppointments.column("Date", width=100)            
    confirmedAppointments.column("Property", width=150)      
    confirmedAppointments.column("Time", width=70)             
    confirmedAppointments.column("Viewer Name", width=120)     
    confirmedAppointments.column("Contact Number", width=110)  
    confirmedAppointments.column("Email Address", width=150)   
    confirmedAppointments.column("Notes", width=200)           
    
    confirmedAppointments.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
    frameR.grid_rowconfigure(0, weight=1)
    frameR.grid_columnconfigure(0, weight=1)

#Output availability dates for booking appointments for next 30 days.
    def loadDataMenu():
        """Populate the date menu with available dates."""
        dates = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(30)]
        dateSelection['values'] = [date.strftime('%Y-%m-%d') for date in dates]
        dateSelection.set(dates[0].strftime('%Y-%m-%d'))

#Retreive property that are available for sale and not sold, to help agent book appointment with clients.
    def loadPropertyMenu():
        """Populate the property menu with available properties."""
        properties = searchProperties()
        propertyMenu['values'] = [f"{prop[0]}: {prop[1]}" for prop in properties]
        # Store properties in a dictionary(dict) using ID which should be independent from the existing property ID, to help track appointments.
        propertyMenu.property_dict = {f"{prop[0]}: {prop[1]}": prop[0] for prop in properties}

#load saved appointment into appointment/diary treeview.
    def loadConfirmedAppointment():
        """Populate the saved appointments treeview with appointments."""
        confirmedAppointments.delete(*confirmedAppointments.get_children())# clear appointments if it has been booked.
        appointments = filterAppointments()# filter appointments in accordances with dates/times etc.
        #this section loops through appointments to replace property ID with property address
        for app in appointments:
            property_address = retreivePropertyAddress(app[2])
            confirmedAppointments.insert("", tk.END, values=(app[0], app[1], property_address, app[3], app[4], app[5], app[6], app[7]))

    def selectedDate(event=None):
        """Update the appointment preview based on the selected date and property."""
        confirmedDate = dateVariable.get()
        selectedProperty = propertyVariable.get()
        property_id = propertyMenu.property_dict.get(selectedProperty, "") if selectedProperty else ""
        confirmedTime = timeVariable.get()
      #FILTER APPOINTMENT WITH CONFIRMED DATE, TIME AND PROPERTY   
        appointments = filterAppointments(date=confirmedDate, property_id=property_id, time=confirmedTime)
       #To help user with managing property appointments. This feature populates relevant fields for appointments that already exist in the 'appointment' database, if the same date/time and property details are inputted in the entry fields.
        if appointments:
            appointment = appointments[0]
            appointmentText.delete("1.0", tk.END)
            inputViewerName.delete(0, tk.END)
            inputViewerContactNumber.delete(0, tk.END)
            emailInput.delete(0, tk.END)
         #Automatically fill matched appointment details in the entry fields.   
            appointmentText.insert(tk.END, appointment[-1])  # Assuming notes are the last column
            inputViewerName.insert(0, appointment[4])
            inputViewerContactNumber.insert(0, appointment[5])
            emailInput.insert(0, appointment[6])
        else:
            appointmentText.delete("1.0", tk.END)
            inputViewerName.delete(0, tk.END)
            inputViewerContactNumber.delete(0, tk.END)
            emailInput.delete(0, tk.END)

    def saveAppointment():
        """Save the appointments for the selected date."""
        confirmedDate = dateVariable.get()
        selectedProperty = propertyVariable.get()
        property_id = propertyMenu.property_dict.get(selectedProperty, "")
        confirmedTime = timeVariable.get()
        viewerName = inputViewerName.get().strip()  # Updated this line to reference inputViewerName
        contactNumber = inputViewerContactNumber.get().strip()
        emailAddress = emailInput.get().strip()
        notes = appointmentText.get("1.0", tk.END).strip()

#All fields are required to be filled for appointment to be saved.
        if not (confirmedDate and confirmedTime and viewerName and contactNumber and emailAddress):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
#Ensure contact number is 11 digits before submitting appointmnet details to database
        if not validateContactNumber(contactNumber):
            messagebox.showerror("Input Error", "Invalid contact number. It must be 11 digits.")
            return

        try:
            time_obj = datetime.datetime.strptime(confirmedTime, "%H:%M").time()
            if not validateAppointmentTime(time_obj):
                raise ValueError("Time out of bounds")
        except ValueError:
            messagebox.showerror("Input Error", "Time must be between 9:00 AM and 3:00 PM.")
            return

        # Save the appointment to the database
        initiateAppointment(confirmedDate, property_id, confirmedTime, viewerName, contactNumber, emailAddress, notes)
        loadConfirmedAppointment()
        messagebox.showinfo("Success", "Appointment saved successfully!")

#if appointment is cancelled, agent is able to delete this effortlessly from treeview.
#before deleting the appointments, this function checks to see if appoitnment is still present in the database.
    def deleteClickedAppointment():
        """Delete the selected appointment from the database."""
        clickedAppointment = confirmedAppointments.selection()
        if not clickedAppointment:
            messagebox.showerror("Selection Error", "No appointment selected.")
            return
        #confirm changes with agent before deleting appointment
        appointment_id = confirmedAppointments.item(clickedAppointment, 'values')[0]  # Assuming ID is the first column
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?"):
            try:
                deleteAppointment(appointment_id)
                loadConfirmedAppointment()
                messagebox.showinfo("Success", "Appointment deleted successfully!")
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete appointment: {e}")
#populate menu and appointment list.
    loadDataMenu()
    loadPropertyMenu()
    loadConfirmedAppointment()

    dateSelection.bind("<<ComboboxSelected>>", selectedDate)
    timeMenu.bind("<<ComboboxSelected>>", selectedDate)
    propertyMenu.bind("<<ComboboxSelected>>", selectedDate)
#Buttons/Widgets to save, delete appointment
    tk.Button(frameL, text="Save Appointment", command=saveAppointment, bg="brown", fg="white").grid(row=15, column=0, pady=10, padx=10)
    tk.Button(frameL, text="Delete Appointment", command=deleteClickedAppointment, bg="red", fg="white").grid(row=16, column=0, pady=10, padx=10)
    tk.Button(appointmentDiary, text="Close", command=appointmentDiary.destroy, bg="brown", fg="white").grid(row=17, column=0, pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)

if __name__ == '__main__':
    root = tk.Tk()
    tk.Button(root, text="Open Diary", command=optimiseDiaryWindow).pack(pady=20)
    root.mainloop()
