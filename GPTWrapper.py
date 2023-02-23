import customtkinter
import requests
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Español
#chat = ["El siguiente es un chatbot amistoso, educado, que responde a cualquier tipo de pregunta. Responde de una forma detallada."]
#English
chat = ["The following is a friendly, polite chatbot that answers any type of question. It answers in a detailed way."]

window = customtkinter.CTk()
window.title("GPT3 Chatbot")
window.minsize(width=400, height=400)

def process_input(*args):
    api = api_key.get()
    
    if not api:
        chat_window.configure(state='normal')
        chat_window.insert(customtkinter.END, "API Error\n", 'bot')
        chat_window.tag_config('bot', background='#00ff99', foreground='black')
        chat_window.configure(state='disabled')
        chat_window.see(customtkinter.END)
        return
    
    chat_window.configure(state='normal')
    chat_window.insert(customtkinter.END, f"{user_entry.get()}\n", 'user')
    chat_window.tag_config('user', background='#0099ff', foreground='white')
    
    def background_thread():
        user_input = str(user_entry.get())
        chat.append("Humano: "+user_input)
        conversation = "\n".join(chat)
        
        user_entry.grid_forget()
        
        progress = customtkinter.CTkProgressBar(window, mode="indeterminate")
        progress.grid(column=0, row=2, columnspan=1, pady=10)
        progress.start()

        try:
            response = requests.post('https://api.openai.com/v1/completions',
                                    json={
                                        'model': 'text-davinci-003',
                                        'prompt': conversation + "\nBot: ",
                                        'max_tokens': 512,
                                        'temperature': 0.7,
                                        'top_p': 1
                                    },
                                    headers={
                                        'Content-Type': 'application/json',
                                        'Authorization': 'Bearer ' + api # API KEY
                                    })
            #tokens = response.json()['usage']['total_tokens']
            response_text = str(response.json()['choices'][0]['text'])
            
            while response_text.startswith("\n"):
                response_text = response_text[1:]
            
            chat_window.insert(customtkinter.END, f"{response_text}\n\n", 'bot')
            chat_window.tag_config('bot', background='#00ff99', foreground='black')
            chat_window.configure(state='disabled')
            chat_window.see(customtkinter.END)
        
            chat.append("Bot: "+response_text)
            
        except:
            chat_window.configure(state='normal')
            chat_window.insert(customtkinter.END, "API Error\n", 'bot')
            chat_window.tag_config('bot', background='#00ff99', foreground='black')
            chat_window.configure(state='disabled')
            chat_window.see(customtkinter.END)
            return
        
        user_entry.delete(0, "end")
        user_entry.grid(column=0, row=2)
         
        progress.stop()
        progress.destroy()

    thread = threading.Thread(target=background_thread)
    thread.start()

font = customtkinter.CTkFont(family='Arial', size=20)
api_key = customtkinter.CTkEntry(window, width=350, show="\u00B7", font=font, placeholder_text="API Key")
api_key.grid(column=0, row=0, columnspan=1, padx=10, pady=10)

chat_window = customtkinter.CTkTextbox(window, width=500, height=500) #,fg_color="white")
chat_window.configure(state='disabled')
chat_window.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

user_entry = customtkinter.CTkEntry(window, width=300)
user_entry.grid(column=0, row=2)
user_entry.bind("<Return>", process_input)

submit_button = customtkinter.CTkButton(window, text="Submit", command=process_input)
submit_button.grid(column=1, row=2, padx=10, pady=10)

window.mainloop()



