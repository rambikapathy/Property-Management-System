import tkinter as tk
import openai
from tkinter import scrolledtext

# Intiate API Key
def userQuestion(question):
    openai.api_key = 'YOUR_OPENAI_API_KEY'  
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I am a chat assistant and am helpful at assisting with property management queries and questions regarding the UK property market industry."},
            {"role": "user", "content": question}
        ]
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    return answer

# Open FAQ window
def chatBotWindow():
    FAQwindow = tk.Toplevel()
    FAQwindow.title("Property Management Chatbot")
    FAQwindow.geometry("500x600")
    FAQwindow.configure(bg="black")

    tk.Label(FAQwindow, text="Please type your query below", bg="black", fg="white", font=("Arial", 14)).pack(pady=10)

    # Text box to allow agent to input query
    queryInput = tk.Entry(FAQwindow, width=50)
    queryInput.pack(pady=10)

    # ScrolledText to display previous chat conversation
    chatHistory = scrolledtext.ScrolledText(FAQwindow, wrap=tk.WORD, width=60, height=20)
    chatHistory.pack(pady=10)
    chatHistory.insert(tk.END, "Chatbot: How can I assist you with property management queries\n")

    # Function that reads and responds to agent queries
    def submitAgentQuery():
        agentQuery = queryInput.get()
        if agentQuery:
            chatHistory.insert(tk.END, f"You: {agentQuery}\n")
            response = userQuestion(agentQuery)
            chatHistory.insert(tk.END, f"Chatbot: {response}\n\n")
            queryInput.delete(0, tk.END)

    tk.Button(FAQwindow, text="Submit", command=submitAgentQuery).pack(pady=10)

    tk.Button(FAQwindow, text="Close Window", command=FAQwindow.destroy).pack(pady=10)
