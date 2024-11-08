import robin_stocks.robinhood as rh
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='trading_bot.log'
)

class RobinhoodBot:
    def __init__(self):
        # Load credentials from .env file
        load_dotenv()
        self.username = os.getenv('RH_USERNAME')
        self.password = os.getenv('RH_PASSWORD')
        self.login()
        
    def login(self):
        """Login to Robinhood"""
        try:
            rh.login(self.username, self.password)
            logging.info("Successfully logged into Robinhood")
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise

    def get_buying_power(self):
        """Get available buying power"""
        return float(rh.load_account_profile()['buying_power'])

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        return float(rh.stocks.get_latest_price(symbol)[0])

    def get_positions(self):
        """Get current positions"""
        return rh.build_holdings()

    def place_buy_order(self, symbol, quantity):
        """Place a buy order"""
        try:
            order = rh.orders.order_buy_market(symbol, quantity)
            logging.info(f"Buy order placed for {quantity} shares of {symbol}")
            return order
        except Exception as e:
            logging.error(f"Buy order failed: {e}")
            return None

    def place_sell_order(self, symbol, quantity):
        """Place a sell order"""
        try:
            order = rh.orders.order_sell_market(symbol, quantity)
            logging.info(f"Sell order placed for {quantity} shares of {symbol}")
            return order
        except Exception as e:
            logging.error(f"Sell order failed: {e}")
            return None

    def simple_moving_average(self, symbol, interval='day', span=20):
        """Calculate simple moving average"""
        hist_data = rh.stocks.get_stock_historicals(symbol, interval=interval)
        prices = [float(item['close_price']) for item in hist_data]
        return np.mean(prices[-span:])

    def check_and_trade(self, symbol, max_position=1000):
        """Main trading logic"""
        try:
            current_price = self.get_current_price(symbol)
            sma = self.simple_moving_average(symbol)
            positions = self.get_positions()
            
            # Check if we already own the stock
            current_position = positions.get(symbol, {'quantity': 0})
            quantity_owned = float(current_position.get('quantity', 0))
            
            if current_price > sma and quantity_owned == 0:
                # Buy signal
                buying_power = self.get_buying_power()
                if buying_power > max_position:
                    quantity = round(max_position / current_price, 2)
                    self.place_buy_order(symbol, quantity)
                    logging.info(f"Buy signal: {symbol} at {current_price}")
                
            elif current_price < sma and quantity_owned > 0:
                # Sell signal
                self.place_sell_order(symbol, quantity_owned)
                logging.info(f"Sell signal: {symbol} at {current_price}")
                
        except Exception as e:
            logging.error(f"Error in check_and_trade: {e}")

    def run(self, symbols=['AAPL', 'MSFT'], interval=300):
        """Run the trading bot"""
        logging.info("Starting trading bot...")
        while True:
            try:
                for symbol in symbols:
                    self.check_and_trade(symbol)
                    logging.info(f"Checked {symbol}")
                time.sleep(interval)  # Wait 5 minutes between checks
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(interval)
                
                
# Create a .env file with:
"""
RH_USERNAME=your_username
RH_PASSWORD=your_password
"""

# Dashboard (simple version)
def print_dashboard():
    bot = RobinhoodBot()
    positions = bot.get_positions()
    buying_power = bot.get_buying_power()
    
    print("\n=== Trading Bot Dashboard ===")
    print(f"Available Buying Power: ${buying_power}")
    print("\nCurrent Positions:")
    for symbol, data in positions.items():
        print(f"{symbol}: {data['quantity']} shares at ${data['average_buy_price']}")

if __name__ == "__main__":
    # To run the dashboard:
    # print_dashboard()
    
    # To run the trading bot:
    bot = RobinhoodBot()
    bot.run(['AAPL', 'MSFT'])  # Add whatever symbols you want to trade
