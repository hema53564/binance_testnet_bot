import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from .trading_bot import BasicBot
import threading

class TradingGUI:
    def __init__(self, root):
        self.root = root
        root.title("Binance Futures Testnet Bot")
        root.geometry("760x520")

        frame_api = ttk.LabelFrame(root, text="API Credentials")
        frame_api.pack(fill="x", padx=10, pady=6)

        ttk.Label(frame_api, text="API Key:").grid(row=0, column=0, sticky="w")
        self.api_key_entry = ttk.Entry(frame_api, width=80)
        self.api_key_entry.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(frame_api, text="API Secret:").grid(row=1, column=0, sticky="w")
        self.api_secret_entry = ttk.Entry(frame_api, width=80, show="*")
        self.api_secret_entry.grid(row=1, column=1, padx=6, pady=4)

        self.connect_btn = ttk.Button(frame_api, text="Connect", command=self.connect)
        self.connect_btn.grid(row=0, column=2, rowspan=2, padx=6)

        frame_order = ttk.LabelFrame(root, text="Place Order")
        frame_order.pack(fill="x", padx=10, pady=6)

        ttk.Label(frame_order, text="Symbol:").grid(row=0, column=0, sticky="w")
        self.symbol_entry = ttk.Entry(frame_order, width=20)
        self.symbol_entry.insert(0, "BTCUSDT")
        self.symbol_entry.grid(row=0, column=1, padx=6)

        ttk.Label(frame_order, text="Side:").grid(row=0, column=2, sticky="w")
        self.side_var = tk.StringVar(value="BUY")
        ttk.OptionMenu(frame_order, self.side_var, "BUY", "BUY", "SELL").grid(row=0, column=3)

        ttk.Label(frame_order, text="Order Type:").grid(row=0, column=4, sticky="w")
        self.otype_var = tk.StringVar(value="MARKET")
        ttk.OptionMenu(frame_order, self.otype_var, "MARKET", "MARKET", "LIMIT", "STOP_LIMIT").grid(row=0, column=5)

        ttk.Label(frame_order, text="Qty:").grid(row=1, column=0, sticky="w")
        self.qty_entry = ttk.Entry(frame_order, width=12)
        self.qty_entry.insert(0, "0.001")
        self.qty_entry.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(frame_order, text="Price:").grid(row=1, column=2, sticky="w")
        self.price_entry = ttk.Entry(frame_order, width=12)
        self.price_entry.grid(row=1, column=3, padx=6)

        ttk.Label(frame_order, text="Stop Price:").grid(row=1, column=4, sticky="w")
        self.stop_entry = ttk.Entry(frame_order, width=12)
        self.stop_entry.grid(row=1, column=5, padx=6)

        self.place_btn = ttk.Button(frame_order, text="Place Order", command=self.on_place_order)
        self.place_btn.grid(row=2, column=0, columnspan=6, pady=8)

        frame_out = ttk.LabelFrame(root, text="Output")
        frame_out.pack(fill="both", expand=True, padx=10, pady=6)
        self.out_text = scrolledtext.ScrolledText(frame_out, state='normal')
        self.out_text.pack(fill="both", expand=True)

        self.bot = None

    def connect(self):
        api_key = self.api_key_entry.get().strip()
        api_secret = self.api_secret_entry.get().strip()
        if not api_key or not api_secret:
            messagebox.showwarning("Missing credentials", "Provide API Key and Secret")
            return
        try:
            self.bot = BasicBot(api_key, api_secret, testnet=True)
            self.append_out("Connected to Binance Futures Testnet")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def append_out(self, msg):
        self.out_text.insert('end', msg + "\n")
        self.out_text.see('end')

    def on_place_order(self):
        if self.bot is None:
            messagebox.showwarning("Not connected", "Please connect first")
            return
        symbol = self.symbol_entry.get().strip().upper()
        side = self.side_var.get().strip().upper()
        otype = self.otype_var.get().strip().upper()
        qty = float(self.qty_entry.get())
        price = self.price_entry.get().strip()
        stop = self.stop_entry.get().strip()
        price = float(price) if price else None
        stop = float(stop) if stop else None
        threading.Thread(target=self._place_order_thread, args=(symbol, side, otype, qty, price, stop), daemon=True).start()

    def _place_order_thread(self, symbol, side, otype, qty, price, stop):
        self.append_out(f"Placing {otype} {side} {symbol} qty={qty}")
        try:
            result = self.bot.place_order(symbol, side, otype, qty, price, stop)
            self.append_out(str(result))
        except Exception as e:
            self.append_out(f"Order failed: {e}")
