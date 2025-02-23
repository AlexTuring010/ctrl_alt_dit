import joblib
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta
import argparse

# Initialize Supabase client
url = "https://fnyguyvlwoixbtmfdala.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZueWd1eXZsd29peGJ0bWZkYWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk5Nzg3MTMsImV4cCI6MjA1NTU1NDcxM30.nyyirErozsVak5S93zTI8hX8R23NxNttu-NTMdjQpEI"
supabase: Client = create_client(url, key)

# Load the saved model
model_file = "./models/budget_model_new.pkl"
model, features_used = joblib.load(model_file)

def fetch_data(customer_id: int, date: str):
    # Calculate the date range for the past 7 days
    end_date = datetime.strptime(date, '%Y-%m-%d').date()
    start_date = end_date - timedelta(days=6)
    
    # Fetch data from Supabase
    response = supabase.table('budget_data').select('*').eq('customer_id', customer_id).gte('date', start_date).lte('date', end_date).execute()
    data = response.data
    
    # Initialize data dictionary with zeros
    data_dict = {
        "win_loss_day1": [0], "win_loss_day2": [0], "win_loss_day3": [0], "win_loss_day4": [0], "win_loss_day5": [0], "win_loss_day6": [0], "win_loss_day7": [0],
        "balance_day1": [0], "balance_day2": [0], "balance_day3": [0], "balance_day4": [0], "balance_day5": [0], "balance_day6": [0], "balance_day7": [0],
        "wage_day1": [0], "wage_day2": [0], "wage_day3": [0], "wage_day4": [0], "wage_day5": [0], "wage_day6": [0], "wage_day7": [0]
    }
    
    # Fill data dictionary with fetched data
    for record in data:
        day_index = (end_date - datetime.strptime(record['date'], '%Y-%m-%d').date()).days
        if 0 <= day_index < 7:
            data_dict[f"win_loss_day{day_index + 1}"][0] = record['win_loss']
            data_dict[f"balance_day{day_index + 1}"][0] = record['balance']
            data_dict[f"wage_day{day_index + 1}"][0] = record['wage']
    
    return data_dict

def predict_budget(customer_id: int, date: str):
    data_dict = fetch_data(customer_id, date)
    input_df = pd.DataFrame(data_dict)
    
    # Ensure that input_df has the same feature columns used in training (features_used).
    input_df = input_df.reindex(columns=features_used, fill_value=0)
    
    # Make prediction
    predicted_budget = model.predict(input_df)[0]
    return predicted_budget

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict weekly budget for a customer.")
    parser.add_argument("customer_id", type=int, help="Customer ID")
    parser.add_argument("date", type=str, help="Date in YYYY-MM-DD format")
    args = parser.parse_args()
    
    predicted_budget = predict_budget(args.customer_id, args.date)
    print(predicted_budget)