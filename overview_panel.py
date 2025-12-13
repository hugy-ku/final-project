from socket_manager import SocketManager
from tkinter import Tk, ttk
import tkinter as tk
import json

class OverviewPanel:
    def __init__(self, master: tk.Frame, symbol_name: str, symbol_id: str):
        self.symbol_name = symbol_name
        self.symbol_id = symbol_id
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.configure(background="#AAAAAA")
        self.socket_manager = SocketManager(f"wss://stream.binance.com:9443/ws/{symbol_id}@ticker", self.on_message)

        self.socket_manager

        self.title = ttk.Label(self.frame, text=self.symbol_name, background="#AAAAAA", font=("TkDefaultFont", 20))
        self.title.pack(expand=True)

        self.current_price = ttk.Label(self.frame, text="---", background="#AAAAAA",font=("TkDefaultFont", 25))
        self.current_price.pack(expand=True)

        self.change = ttk.Label(self.frame, text="--- (---%)", background="#AAAAAA", font=("TkDefaultFont", 10))
        self.change.pack(expand=True)
    
    def on_message(self, ws, message):
        message = json.loads(message)
        self.frame.after(0, lambda: self.update_text(message))

    def update_text(self, message):
        current_price = message["c"].rstrip("0")
        change = message["p"].rstrip("0")
        percent = message["P"]
        
        try:
            current_price = float(current_price)
            change = float(change)
            percent = float(percent)
        except ValueError:
            print("Error: change is not a float")
            return
        if change > 0:
            colour = "#00B500"
        elif change < 0:
            colour = "#DD0000"
        else:
            colour = "#000000"

        self.current_price.configure(text=f"{current_price:.2f}", foreground=colour)
        self.change.configure(text=f"{change:.2f} ({percent:.2f}%)", foreground=colour)


    def stop(self):
        self.socket_manager.stop()
        try:
            self.frame.grid_forget()
        except tk.TclError:
            pass
        print(f"Panel [{self.symbol_id}] has been unloaded")


if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    try:    
        manager = OverviewPanel(frame, "btcusdt")
        root.mainloop()
    except Exception as e:
        print(f"\n{'#'*10}ERROR{'#'*10}")
        print(e)
        print(f"{'#'*25}\n")
    finally:
        manager.stop()        
