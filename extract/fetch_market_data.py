import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

def fetch_daily_data(symbol="IBM"):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully fetched {symbol} data!")
        return data
    else:
        print(f"API request failed with status {response.status_code}.")
        return None

def save_raw_data(data, symbol="IBM"):
    if not data:
        return
        
    # Create a directory for the raw data lake
    os.makedirs("data/raw", exist_ok=True)
    
    # Generate a filename with today's date
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"data/raw/{symbol}_{date_str}.json"
    
    # Save the raw JSON data
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Raw data successfully saved to {filename}")

if __name__ == "__main__":
    market_data = fetch_daily_data()
    save_raw_data(market_data)