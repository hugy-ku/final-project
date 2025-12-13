from tkinter import Tk, ttk
import tkinter as tk

class TitleBar:
    def __init__(self, master: Tk, button_names: dict, button_event):
        self.button_event = button_event
        self.buttons = {}
        self.master = master
        self.master.configure(bg="#555555")
        
        default_button = tk.Button(self.master)
        self.default_background = default_button["bg"]
        self.default_foreground = default_button["fg"]

        title = tk.Label(self.master, text="Crypto Board", foreground="#FFFFFF", background="#555555", font=("TkDefaultFont", 20))
        title.pack(side="left")

        page_select = tk.Frame(self.master, background="#555555")
        page_select.pack(side="left", expand=True, padx=10)

        overview_button = tk.Button(page_select, text="Overview", command=lambda: self.button_event("overview"), width=8)
        overview_button.grid(row=0, pady=2)
        self.buttons["overview"] = overview_button

        order_book_button = tk.Button(page_select, text="Order Book", command=lambda: self.button_event("order_book"), width=8)
        order_book_button.grid(row=1, pady=2)
        self.buttons["order_book"] = order_book_button

        button_frame = tk.Frame(self.master, background="#555555")
        button_frame.pack(side="right")
        self.load_buttons(button_frame, button_names)
    
    def load_buttons(self, master, button_names: dict):
        half = len(button_names)//2 + len(button_names)%2
        for i, button_info in enumerate(button_names.values()):
            row = i // half
            column = i % half
            button_id = button_info["id"]
            button_name = button_info["name"]
            button = tk.Button(
                master,
                text=button_name,
                # stackoverflow saves the day yet again
                command=lambda id=button_id: self.button_event(id),
                width=8
            )
            self.buttons[button_id] = button
            button.grid(row=row, column=column, padx=2, pady=2)

    def change_button_colour(self, button_id, mode="unpressed"):
        if mode == "unpressed": 
            background = self.default_background
            foreground=self.default_foreground
        if mode == "pressed": 
            background = self.default_foreground
            foreground=self.default_background
        self.buttons[button_id].configure(background=background, foreground=foreground, activebackground=background, activeforeground=foreground)


if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x100")
    SYMBOLS = {
        "btcusdt": {"name": "BTC/USDT", "id": "btcusdt"},
        "ethusdt": {"name": "ETH/USDT", "id": "ethusdt"},
        "solusdt": {"name": "SOL/USDT", "id": "solusdt"},
        "bnbusdt": {"name": "BNB/USDT", "id": "bnbusdt"},
        "btcusdc": {"name": "BTC/USDC", "id": "btcusdc"},
        "ethusdc": {"name": "ETH/USDC", "id": "ethusdc"},
        "solusdc": {"name": "SOL/USDC", "id": "solusdc"},
        "bnbusdc": {"name": "BNB/USDC", "id": "bnbusdc"},
    }
    title_bar = TitleBar(root, SYMBOLS, lambda name: print(f"{name} pressed"))
    root.mainloop()
