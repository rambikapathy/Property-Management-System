import tkinter as tk
from tkinter import scrolledtext

#function to iniate query response.
def initiateresponses(file_path):
    responses = {}#optimise empty dictionary for new chat thread.
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '|' in line:
                    #split the line into queries
                    query, response = line.strip().split('|', 1)
                    responses[query.lower()] = response
    except FileNotFoundError:
        #if response.txt not found, output error message.
        print(f"Error: {file_path} not found.")
    return responses

#function to output response to query by retireving answers from 'responses.txt' file.
def retreiveResponse(query, responses):
    query = query.lower()
    return responses.get(query, "I'm sorry, I don't have an answer to your query. Please try another query or contact your manager.")#if answer does not exist, output error message.

#function for agent to input query.
def inputMessage():
    user_input = entryBox.get("1.0", 'end-1c').strip()
    if user_input:
        chatThread.config(state=tk.NORMAL)
        chatThread.insert(tk.END, "You: " + user_input + '\n\n')
        response = retreiveResponse(user_input, responses)
        chatThread.insert(tk.END, "Bot: " + response + '\n\n')
        chatThread.config(state=tk.DISABLED)
        chatThread.yview(tk.END)#thread that outputs previous chat responses 
        entryBox.delete("1.0", tk.END)#entry box for user to type query.

#function to optimise chatbot window.
def optimiseFAQ_ChatbotWindow():
    global chatThread, entryBox, responses

    # upload answers to queries from text file.
    responses = initiateresponses('responses.txt')
    root = tk.Tk()
    root.title("Rishi's Property Management Chatbot")
    root.geometry("500x600")

    # Chat thread
    chatThread = scrolledtext.ScrolledText(root, bd=1, bg="white", width=50, height=8, font=("Arial", 12))
    chatThread.config(state=tk.DISABLED)

    #Entry box
    entryBox = tk.Text(root, bd=0, bg="white", width=29, height=2, font=("Arial", 12))
    #Buttons
    submitButton = tk.Button(root, font=("Arial", 12, 'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command=inputMessage)
    chatThread.place(x=6, y=6, height=500, width=480)
    entryBox.place(x=6, y=520, height=70, width=380)
    submitButton.place(x=390, y=520, height=70)

    root.mainloop()

if __name__ == "__main__":
    optimiseFAQ_ChatbotWindow()
