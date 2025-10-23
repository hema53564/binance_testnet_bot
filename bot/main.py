import argparse
from tkinter import Tk
from .ui import TradingGUI
from dotenv import load_dotenv
import os
load_dotenv()
def run_gui():
    root = Tk()
    app = TradingGUI(root)
    root.mainloop()

def run_cli():
    from .trading_bot import BasicBot
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    bot = BasicBot(api_key, api_secret, testnet=True)
    while True:
        print("1. MARKET 2. LIMIT 3. STOP_LIMIT 4. Exit")
        c = input("Choice: ")
        if c == '4': break
        sym = input("Symbol: ").upper()
        side = input("Side (BUY/SELL): ").upper()
        qty = float(input("Qty: "))
        if c == '1':
            bot.place_order(sym, side, 'MARKET', qty)
        elif c == '2':
            p = float(input("Price: "))
            bot.place_order(sym, side, 'LIMIT', qty, p)
        elif c == '3':
            p = float(input("Price: "))
            s = float(input("Stop Price: "))
            bot.place_order(sym, side, 'STOP_LIMIT', qty, p, s)
        else:
            print("Invalid")
if __name__ == "__main__":
    mode = input("Choose mode (CLI/GUI): ").strip().upper()
    if mode == "CLI":
        run_cli()
    elif mode == "GUI":
        run_gui()
    else:
        print("Invalid choice. Exiting...")
