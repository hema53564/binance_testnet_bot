import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger("trading_bot")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/trading_bot.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        try:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        except Exception:
            logger.warning("Could not set FUTURES_URL, check library version")
        logger.info("BasicBot initialized (testnet=%s)", testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        side = side.upper()
        order_type = order_type.upper()
        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        if order_type == "MARKET":
            payload = dict(symbol=symbol, side=side, type="MARKET", quantity=quantity)
        elif order_type == "LIMIT":
            if price is None:
                raise ValueError("Price required for LIMIT orders")
            payload = dict(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", quantity=quantity, price=str(price))
        elif order_type == "STOP_LIMIT":
            if stop_price is None or price is None:
                raise ValueError("Stop price and price required for STOP_LIMIT orders")
            payload = dict(symbol=symbol, side=side, type="STOP", timeInForce="GTC", quantity=quantity, price=str(price), stopPrice=str(stop_price))
        else:
            raise ValueError("Invalid order type")

        logger.info("Placing order: %s", payload)
        try:
            order = self.client.futures_create_order(**payload)
            logger.info("Order response: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("BinanceAPIException: %s", e)
            raise
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            raise
