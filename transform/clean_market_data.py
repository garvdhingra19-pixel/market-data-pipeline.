import json
import pandas as pd
import glob
import os

def transform_data():
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        print("No raw data found!")
        return
        
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        raw_data = json.load(f)
        
    # 1. Stop the script gracefully if the API returned an error/rate limit
    time_series = raw_data.get("Time Series (Daily)", {})
    if not time_series:
        print("Error: API did not return time series data. You may be rate-limited.")
        print(f"Raw API Response: {raw_data}")
        return
        
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = [col.split(' ')[1] for col in df.columns]
    
    # 2. Fix the Pandas deprecation warnings by avoiding inplace=True
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    
    df['date'] = pd.to_datetime(df['date'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
        
    os.makedirs('data/transformed', exist_ok=True)
    output_path = 'data/transformed/IBM_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"Data successfully transformed and saved to {output_path}")

if __name__ == "__main__":
    transform_data()