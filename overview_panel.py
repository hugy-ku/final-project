from socket_manager import SocketManager
import tkinter as tk
import json
from time import sleep
import threading

class OverviewPanel:
    def __init__(self, master: tk.Frame, symbol_name: str, symbol_id: str):
        self.symbol_name = symbol_name
        self.symbol_id = symbol_id
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.configure(background="#AAAAAA")
        self.socket_manager = SocketManager(f"wss://stream.binance.com:9443/ws/{symbol_id}@ticker", self.on_message, self.on_close, self.on_open)

        self.status_frame = tk.Frame(self.frame, background="#AAAAAA")
        self.status_frame.pack(expand=True, fill="x")
        self.reconnect_button = tk.Button(self.status_frame, command=threading.Thread(target=self.reconnect).start, text="reconnect",background="#AAAAAA")
        self.status = tk.Label(self.status_frame, text="Disconnected", background="#AAAAAA", foreground="#DD0000")
        self.reconnect_button.pack(side="left", padx=5)
        self.status.pack(side="right", padx=5)

        self.title = tk.Label(self.frame, text=self.symbol_name, background="#AAAAAA", font=("TkDefaultFont", 20))
        self.title.pack(expand=True)

        self.current_price = tk.Label(self.frame, text="---", background="#AAAAAA",font=("TkDefaultFont", 25))
        self.current_price.pack(expand=True)

        self.change = tk.Label(self.frame, text="--- (---%)", background="#AAAAAA", font=("TkDefaultFont", 10))
        self.change.pack(expand=True)

    def reconnect(self):
        if self.socket_manager.ws:
            self.socket_manager.stop()
        sleep(1) # placebo :P
        self.socket_manager.start()

    def set_status(self, connected: bool):
        if connected:
            self.status.configure(text="connected", foreground="#00B500")
        elif not connected:
            self.status.configure(text="disconnected", foreground="#DD0000")

    def on_message(self, ws, message):
        message = json.loads(message)
        self.frame.after(0, lambda: self.update_text(message))

    def on_close(self, ws, s, m):
        print(f"{self.socket_manager.url} has closed")
        self.frame.after(0, self.set_status(False))

    def on_open(self, ws):
        print(f"{self.socket_manager.url} has connected")
        self.frame.after(0, self.set_status(True))

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
    root = tk.Tk()
    root.geometry("800x600")
    try:
        manager = OverviewPanel(root, "BTC/USDT", "btcusdt")
        # it looks stupid but its only been 3 days since I started and I'm not refactoring everything already
        manager.frame.pack(expand=True, fill="both")
        root.mainloop()
    except Exception as e:
        print(f"\n{'#'*10}ERROR{'#'*10}")
        print(e)
        print(f"{'#'*25}\n")
    finally:
        manager.stop()
