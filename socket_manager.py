import websocket
import threading
import time


class SocketManager():
    def __init__(self, url: str, on_message, on_close=None, on_open=None):
        self.url = url
        self.on_message = on_message
        if on_close: self.on_close = on_close
        if on_open: self.on_open = on_open
        self.ws = None
        self.start()


    def on_error(self, ws, error):
        print(f"{self.url} error: {error}")
        ws = None

    def on_close(self, ws, s, m):
        print(f"{self.url} has closed")

    def on_open(self, ws):
        print(f"{self.url} has connected")

    def start(self):
        if self.ws:
            return

        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def stop(self):
        # you have to do this otherwise on_close doesn't trigger
        def run(*args):
            if self.ws:
                self.ws.close()
                self.ws = None
        threading.Thread(target=run).start()


if __name__ == "__main__":
    url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

    def on_message(ws, message):
        print(message)

    ws = SocketManager(url, on_message)

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"\n{'#'*10}ERROR{'#'*10}")
        print(e)
        print(f"{'#'*25}\n")
    finally:
        ws.stop()
