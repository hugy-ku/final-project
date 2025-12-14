import tkinter as tk
from title_bar import TitleBar
from overview_manager import OverviewManager
from order_book_manager import OrderBook

class CryptoBoard:
    def __init__(self, master: tk.Frame, symbols):
        self.master = master
        self.master.geometry("1100x600")
        self.symbols = symbols

        self.mode = None

        self.title_frame = tk.Frame(self.master)
        self.title_frame.pack(fill="x")
        self.title_bar = TitleBar(self.title_frame, symbols, self.on_button_pressed)

        self.overview_frame = tk.Frame(self.master)
        self.overview_frame.pack(side="right", expand=True, fill="both")
        self.overview_manager = OverviewManager(self.overview_frame, self.symbols)

        self.order_book_frame = tk.Frame(self.master)
        self.order_book = None

        self.load_preferences()
        self.master.mainloop()

    def on_button_pressed(self, button_id):
        if button_id == "order_book":
            self.mode = "order_book"
            self.title_bar.change_button_colour("order_book", "pressed")
            self.title_bar.change_button_colour("overview", "unpressed")
            self.save_preferences()
            return
        if button_id == "overview":
            self.mode = "overview"
            self.title_bar.change_button_colour("overview", "pressed")
            self.title_bar.change_button_colour("order_book", "unpressed")
            self.save_preferences()
            return

        if self.mode == "overview":
            found = False
            for panel in self.overview_manager.panels:
                if panel.symbol_id == button_id:
                    found = True
                    break
            if not found:
                self.overview_manager.load_panel(button_id)
            else:
                self.overview_manager.unload_panel(panel)
            self.save_preferences()
            return

        if self.mode == "order_book":
            if self.order_book:
                self.order_book.stop()
                if button_id == self.order_book.symbol_id:
                    self.order_book.stop()
                    self.order_book = None
                    self.save_preferences()
                    return
            self.order_book_frame = tk.Frame(self.master)
            self.order_book = OrderBook(self.order_book_frame, button_id, self.symbols[button_id])
            self.save_preferences()
            return

    def save_preferences(self):
        new_text = []
        new_text.append(self.mode)
        temp = ','.join([panel.symbol_id for panel in self.overview_manager.panels])
        new_text.append(temp)
        if not self.order_book:
            new_text.append("")
        else:
            new_text.append(self.order_book.symbol_id)

        with open("preferences.txt", "w") as file:
            file.write('\n'.join(new_text))


    def load_preferences(self):
        error = False
        try:
            with open("preferences.txt", "r") as file:
                text = file.read().split("\n")
        except FileNotFoundError:
            print("Warning: file not found")
            text = ""
            error = True
        if len(text) != 3:
            error = True
        if error:
            print("Warning: file corrupted")
            self.mode = "overview"
            self.on_button_pressed(self.mode)
            return

        self.overview_manager.load_panels(text[1].split(","))
        if text[2] in self.symbols.keys():
            self.order_book = OrderBook(self.order_book_frame, text[2], self.symbols[text[2]])
        if text[0] in {"overview", "order_book"}:
            self.on_button_pressed(text[0]) # insane code lmao, might fix later (read: never)


if __name__ == "__main__":
    # no idea why i did this
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
    try:
        board = CryptoBoard(root, SYMBOLS)
    except Exception as e:
        print(f"\n{'#'*10}ERROR{'#'*10}")
        print(e)
        print(f"{'#'*25}\n")
    finally:
        if board.order_book:
            board.order_book.stop()
        board.overview_manager.unload_panels()
