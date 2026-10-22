import json
import pandas as pd
import glob
import os

def transform_data():
    # 1. Find the most recent JSON file in the raw data lake
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        print("No raw data found!")
        return
    latest_file = max(list_of_files, key=os.path.getctime)
    
    # 2. Read the raw JSON
    with open(latest_file, 'r') as f:
        raw_data = json.load(f)
        
    # 3. Extract just the nested Time Series dictionary
    time_series = raw_data.get("Time Series (Daily)", {})
    
    # 4. Convert to a Pandas DataFrame
    # orient='index' turns the date keys into rows
    df = pd.DataFrame.from_dict(time_series, orient='index')
    
    # 5. Clean the dataset
    # Remove the numbers from column names (e.g., "1. open" -> "open")
    df.columns = [col.split(' ')[1] for col in df.columns]
    
    # Pull the dates out of the index and into a proper column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'date'}, inplace=True)
    
    # Convert string values to proper mathematical datatypes
    df['date'] = pd.to_datetime(df['date'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
        
    # 6. Save the cleaned, flat table
    output_path = 'data/transformed/IBM_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"Data successfully transformed and saved to {output_path}")
    print(df.head())

if __name__ == "__main__":
    transform_data()