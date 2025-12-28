import tkinter as tk
from tkinter import scrolledtext
import logging

class ModernChatGUI:
    def __init__(self, root, bot_brain):
        self.bot = bot_brain 
        self.root = root
        self.root.title("ProBot - Tech")
        self.root.geometry("450x650")
        self.root.configure(bg="#1e1e2e")

        tk.Label(root, text="🤖 ProBot Assistant", font=("Helvetica", 16, "bold"),
                 bg="#1e1e2e", fg="#89b4fa", pady=20).pack()

        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state='disabled', 
            bg="#313244", fg="#cdd6f4", font=("Segoe UI", 11),
            padx=15, pady=15, borderwidth=0, highlightthickness=0
        )
        self.chat_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.chat_area.tag_configure("user", foreground="#a6e3a1", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_configure("bot", foreground="#89b4fa", font=("Segoe UI", 11, "bold"))

        self.input_frame = tk.Frame(root, bg="#1e1e2e")
        self.input_frame.pack(fill=tk.X, padx=20, pady=(10, 20)) 

        self.user_entry = tk.Entry(
            self.input_frame, font=("Segoe UI", 10), bg="#45475a", 
            fg="#cdd6f4", insertbackground="white", borderwidth=0, relief=tk.FLAT
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=15, padx=(0, 10))
        self.user_entry.bind("<Return>", lambda event: self.send_action())

        self.send_btn = tk.Button(
            self.input_frame, text="SEND", command=self.send_action,
            bg="#89b4fa", fg="#11111b", font=("Helvetica", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=20, pady=8 
        )
        self.send_btn.pack(side=tk.RIGHT)

        self.insert_message("Bot", "System initialized. How can I assist you?")

    def insert_message(self, sender, message):
        self.chat_area.config(state='normal')
        tag = "user" if sender == "You" else "bot"
        self.chat_area.insert(tk.END, f"{sender}: ", tag)
        self.chat_area.insert(tk.END, f"{message}\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

        logging.info(f"{sender}: {message}")

    def send_action(self):
        input_text = self.user_entry.get().strip()
        if not input_text: return

        self.insert_message("You", input_text)
        self.user_entry.delete(0, tk.END)

        response, should_exit = self.bot.get_response(input_text)
        
        self.insert_message("Bot", response)
        if should_exit:
            self.root.after(1500, self.root.destroy)