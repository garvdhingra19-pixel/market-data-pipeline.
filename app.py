import streamlit as st
import pandas as pd
import boto3
import io
import os

st.set_page_config(page_title="Market Data Dashboard")
st.title("IBM Daily Market Data")

# Initialize S3 client using your credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

bucket_name = 'market-data-pipeline-garv-2026'
file_key = 'processed/IBM_cleaned.csv'

try:
    # Fetch the cleaned CSV from your bucket
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    csv_content = response['Body'].read()
    
    # Load into Pandas and display the dashboard elements
    df = pd.read_csv(io.BytesIO(csv_content))
    
    st.write("Raw Dataset")
    st.dataframe(df)
    
    st.write("Closing Price Trend")
    st.line_chart(df.set_index('date')['close'])
    
except Exception as e:
    st.error(f"Error loading data from S3: {e}")