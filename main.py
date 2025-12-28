from bot_logic import SituationalBot
import logging
import tkinter as tk
from ui_design import ModernChatGUI

logging.basicConfig(
    filename='chat_history.log',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

if __name__ == "__main__":
    bot_instance = SituationalBot('data.json')    
    root = tk.Tk()
    app = ModernChatGUI(root, bot_instance) 
    root.mainloop()