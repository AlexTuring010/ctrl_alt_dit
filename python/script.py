import argparse
import numpy as np
import pandas as pd
import pickle
from supabase import create_client, Client
from datetime import datetime, timedelta

# Initialize Supabase client
url = "https://fnyguyvlwoixbtmfdala.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZueWd1eXZsd29peGJ0bWZkYWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk5Nzg3MTMsImV4cCI6MjA1NTU1NDcxM30.nyyirErozsVak5S93zTI8hX8R23NxNttu-NTMdjQpEI"
supabase: Client = create_client(url, key)

def load_model_and_scaler(model_path='./models/svm_model.pkl', scaler_path='./models/scaler.pkl'):
    # Load the trained SVM model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    # Load the scaler
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

def fetch_data(customer_id: int, date: str):
    # Calculate the date range for the past 7 days
    end_date = datetime.strptime(date, '%Y-%m-%d').date()
    start_date = end_date - timedelta(days=6)
    
    # Fetch data from budget_data
    budget_response = supabase.table('budget_data').select('*').eq('customer_id', customer_id).gte('date', start_date).lte('date', end_date).execute()
    budget_data = budget_response.data
    
    # Fetch data from transactions
    transactions_response = supabase.table('transactions').select('*').eq('customer_id', customer_id).gte('date', start_date).lte('date', end_date).eq('event_type', 0).execute()
    transactions_data = transactions_response.data
    
    # Initialize data dictionary with zeros
    data_dict = {
        "bets_amount_7_avg": [0] * 7,
        "daily_average_wager_7_avg": [0] * 7
    }
    
    # Fill data dictionary with fetched budget data
    for record in budget_data:
        day_index = (end_date - datetime.strptime(record['date'], '%Y-%m-%d').date()).days
        if 0 <= day_index < 7:
            data_dict["daily_average_wager_7_avg"][day_index] = record['wage']
    
    # Fill data dictionary with fetched transactions data
    for record in transactions_data:
        day_index = (end_date - datetime.strptime(record['date'], '%Y-%m-%d').date()).days
        if 0 <= day_index < 7:
            data_dict["bets_amount_7_avg"][day_index] += 1  # Increment the count for each bet
    
    # Calculate the average values
    bets_avg = np.mean(data_dict["bets_amount_7_avg"])
    wager_avg = np.mean(data_dict["daily_average_wager_7_avg"])
    
    return bets_avg, wager_avg

def predict_flag(bets, wager, model, scaler, threshold=0.5):
    # Create a DataFrame with column names matching the training data
    input_features = pd.DataFrame([[bets, wager]], columns=['bets_amount_7_avg', 'daily_average_wager_7_avg'])
    
    # Scale the features using the loaded scaler
    input_scaled = scaler.transform(input_features)
    
    # Predict the probability for the positive class (flagged)
    prob_flagged = model.predict_proba(input_scaled)[0, 1]
    
    # Convert probability to a binary decision using the threshold
    prediction = 1 if prob_flagged >= threshold else 0
    
    return prediction, prob_flagged

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Predict if a row is flagged based on bets_amount_7_avg and daily_average_wager_7_avg"
    )
    parser.add_argument('--customer_id', type=int, required=True, help="Customer ID")
    parser.add_argument('--date', type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument('--threshold', type=float, default=0.0043, help="Decision threshold (default: 0.5)")
    
    args = parser.parse_args()
    
    # Load the pre-trained model and scaler
    model, scaler = load_model_and_scaler()
    
    # Fetch data from the database
    bets_avg, wager_avg = fetch_data(args.customer_id, args.date)
    
    # Get prediction
    prediction, prob = predict_flag(bets_avg, wager_avg, model, scaler, args.threshold)
    
    # Output the result
    result = "FLAGGED" if prediction == 1 else "NOT FLAGGED"
    print(f"{prob:.4f},{result}")

if __name__ == "__main__":
    main()