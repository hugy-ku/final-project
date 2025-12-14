import tkinter as tk
from overview_panel import OverviewPanel

class OverviewManager:
    def __init__(self, master: tk.Frame, symbols: dict):
        self.frame = tk.Frame(master)
        self.frame.configure(background="#222222")
        self.frame.pack(expand=True, fill="both")

        self.symbols = symbols
        self.panels = []

    def load_panel(self, symbol_id):
        if symbol_id not in self.symbols.keys():
            return
        panel = OverviewPanel(self.frame, self.symbols[symbol_id], symbol_id)
        self.grid(panel, len(self.panels))
        self.panels.append(panel)

    def unload_panel(self, panel: OverviewPanel):
        panel.stop()
        self.panels.remove(panel)
        self.regrid()

    def grid(self, panel, panel_num):
        row = panel_num % 2
        column = panel_num // 2
        # technically inefficient but the code is much cleaner
        self.frame.rowconfigure(row, weight=1)
        self.frame.columnconfigure(column, weight=1)
        panel.frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    def regrid(self):
        for panel_num, panel in enumerate(self.panels):
            # this took me 2 hours to figure out
            row = (panel_num+1) % 2
            column = (panel_num+1) // 2
            self.frame.rowconfigure(row, weight=0)
            self.frame.columnconfigure(column, weight=0)
            panel.frame.forget()
        for i, panel in enumerate(self.panels):
            self.grid(panel, i)


    def on_button_pressed(self, button_id):
        found = False
        for panel in self.panels:
            if panel.symbol_id == button_id:
                found = True
                break
        if not found:
            self.load_panel(button_id)
            return
        else:
            self.unload_panel(panel)
            return

    def unload_panels(self):
        for panel in self.panels:
            panel.stop()
        self.panels = []

    def load_panels(self, symbol_ids):
        for symbol_id in symbol_ids:
            self.load_panel(symbol_id)

if __name__ == "__main__":
    SYMBOLS = {
        "btcusdt": "BTC/USDT",
        "ethusdt": "ETH/USDT",
        "solusdt": "SOL/USDT",
        "bnbusdt": "BNB/USDT",
        "btcusdc": "BTC/USDC",
        "ethusdc": "ETH/USDC",
        "solusdc": "SOL/USDC",
        "bnbusdc": "BNB/USDC",
    }
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    try:
        board = OverviewManager(frame, SYMBOLS)
        board.load_panel("btcusdt")
        board.load_panel("ethusdt")
        board.load_panel("solusdt")
        root.mainloop()
    except Exception as e:
        print(f"\n{'#'*10}ERROR{'#'*10}")
        print(e)
        print(f"{'#'*25}\n")
    finally:
        board.unload_panels()
