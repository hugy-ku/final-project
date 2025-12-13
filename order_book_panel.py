import tkinter as tk

class OrderBookPanel:
    def __init__(self, master: tk.Frame, depth: int):
        self.master = master
        self.master.pack(expand=True, fill="both")
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.depth = depth

        self.price_label = tk.Label(master, text="price", background="#999999")
        self.amount_label = tk.Label(master, text="amount", background="#999999")
        self.price_label.grid(row=0, column=0, sticky="w", padx=5)
        self.amount_label.grid(row=0, column=1, sticky="e", padx=5)

        self.orders = []
        for i in range(self.depth):
            order_price = tk.Label(self.master, text="", background="#999999")
            order_amount = tk.Label(self.master, text="", background="#999999")
            order_price.grid(row=i+1, column=0, sticky="w", padx=5)
            order_amount.grid(row=i+1, column=1, sticky="e", padx=5)
            self.orders.append([order_price, order_amount])


    def update_orders(self, orders: list):
        for i, order in enumerate(orders):
            order[0] = order[0].rstrip("0")
            if order[0][-1] == ".": order[0] += "0"
            order[1] = order[1].rstrip("0")
            if order[1][-1] == ".": order[1] += "0"
            self.orders[i][0].configure(text=order[0])
            self.orders[i][1].configure(text=order[1])


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    panel = OrderBookPanel(frame)
    root.mainloop()