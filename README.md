# Binance Futures Testnet Trading Bot
This is a simplified trading bot for Binance Futures Testnet (USDT-M) with a Tkinter GUI and CLI fallback.

## Setup

# 1. Create virtual environment (optional but recommended)
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup your API keys
# Copy .env.example to .env in the project root
# Linux/Mac:
cp .env.example .env
# Windows:
copy .env.example .env

# Open .env and replace the placeholder values with your own Binance Testnet API key and secret
# Example:
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret_key

# ⚠️ Do NOT share your .env file. It is ignored by Git (.gitignore) to keep your keys safe.

# 4. Run the bot
python -m bot.main

# 5. To use CLI mode only
python -m bot.main

# 6. To use GUI mode only
python -m bot.ui

# Logs
# Logs will appear in logs/trading_bot.log
# Make sure the logs/ folder exists — the bot creates the log file automatically if it doesn’t exist.

## Notes
# - The repository does NOT include real API keys.
# - To test the bot, you must use your own Binance Testnet API keys.
⚠️ Note: The sample log shows API errors because placeholder API keys were used. 
To see live trading orders, please use your own Binance Testnet API_KEY and API_SECRET in the .env file.

