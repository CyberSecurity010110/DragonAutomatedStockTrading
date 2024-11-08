# DragonAutomatedStockTrading

To use this:

    Create a new directory and navigate to it:

bash

mkdir trading_bot
cd trading_bot

    Create a virtual environment:

bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

    Create requirements.txt and install dependencies:

bash

pip install -r requirements.txt

    Create a .env file with your Robinhood credentials:

RH_USERNAME=your_email
RH_PASSWORD=your_password

    Run the bot:

bash

python Robinhood_DragonTrading_Bot.py

This bot:

    Uses a simple moving average strategy
    Trades specified symbols
    Has basic risk management
    Logs all activities
    Includes a simple dashboard
    Has error handling
