import tkinter as tk
from socket_manager import SocketManager
from order_book_panel import OrderBookPanel
import json

class OrderBook:
    # one of the worst inits I ever created
    def __init__(self, master: tk.Frame, symbol_id, symbol_name, depth=10, interval_ms = 1000):
        self.master = master
        self.symbol_id = symbol_id
        self.symbol_name = symbol_name
        self.depth = depth
        self.url = f"wss://stream.binance.com:9443/ws/{self.symbol_id}@depth{self.depth}@{interval_ms}ms"
        self.ws = SocketManager(self.url, self.on_message)

        self.master.configure(background="#222222")
        self.master.pack(fill="both", expand=True)

        self.title_frame = tk.Frame(self.master, background="#222222")
        self.title_frame.pack(fill="x", pady=5)

        self.title = tk.Label(self.title_frame, text=self.symbol_name, foreground="#FFFFFF", background="#333333")
        self.title.pack(fill="x", padx=5, pady=5)

        self.buy_label = tk.Label(self.title_frame, text="bids", foreground="#00CC00", background="#333333")
        self.sell_label = tk.Label(self.title_frame, text="asks", foreground="#CC0000", background="#333333")
        self.buy_label.pack(side="left", expand=True, fill="both", padx=5)
        self.sell_label.pack(side="right", expand=True, fill="both", padx=5)

        self.buy_frame = tk.Frame(self.master)
        self.buy_frame.pack(side="left", expand=True, fill="both", padx=5, pady=(0,10))
        self.buy_panel = OrderBookPanel(self.buy_frame, depth)

        self.sell_frame = tk.Frame(self.master)
        self.sell_frame.pack(side="right", expand=True, fill="both", padx=5, pady=(0,10))
        self.sell_panel = OrderBookPanel(self.sell_frame, depth)

    def on_message(self, ws, message):
        message = json.loads(message)
        self.master.after(0, lambda: self.buy_panel.update_orders(message["bids"]))
        self.master.after(0, lambda: self.sell_panel.update_orders(message["asks"]))

    def stop(self):
        self.ws.stop()
        try:
            self.master.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    try:
        root = tk.Tk()
        frame = tk.Frame(root)
        book = OrderBook(frame, "btcusdt", "BTC/USDT")
        root.mainloop()
    except Exception as e:
        print(e)
    finally:
        book.stop()