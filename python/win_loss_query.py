import joblib
import pandas as pd
import sys
from datetime import datetime, timedelta
from supabase import create_client, Client

# Initialize Supabase client
url = "your_supabase_url"
key = "your_supabase_key"
supabase: Client = create_client(url, key)

def get_user_data(user_id):
    # Calculate the date range for the past 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)

    # Query the transactions table to get transaction_ids for the past 7 days for the given user
    transactions_query = supabase.table('transactions').select('transaction_id, date').eq('customer_id', user_id).gte('date', start_date).lte('date', end_date).execute()
    transactions_data = transactions_query.data

    # Extract transaction_ids
    transaction_ids = [transaction['transaction_id'] for transaction in transactions_data]

    if not transaction_ids:
        # If no transactions found, return zeroed win_loss_data
        return {f"win_loss_day{i+1}": 0 for i in range(7)}

    # Query the bets table to get win_loss_amount for the extracted transaction_ids
    bets_query = supabase.table('bets').select('transaction_id, win_loss_amount').in_('transaction_id', transaction_ids).execute()
    bets_data = bets_query.data

    # Initialize a dictionary to store win_loss_amount for each day
    win_loss_data = {f"win_loss_day{i+1}": 0 for i in range(7)}

    # Aggregate win_loss_amount for each day
    for bet in bets_data:
        # Find the corresponding transaction date
        transaction = next((t for t in transactions_data if t['transaction_id'] == bet['transaction_id']), None)
        if transaction:
            bet_date = datetime.strptime(transaction['date'], '%Y-%m-%d').date()
            day_index = (bet_date - start_date).days
            win_loss_data[f"win_loss_day{day_index+1}"] += bet['win_loss_amount']

    return win_loss_data

def main(user_id):
    # Load the saved model
    model_file = "budget_model_new.pkl"
    model, features_used = joblib.load(model_file)

    # Get user data
    user_data = get_user_data(user_id)

    # Prepare input data for the model
    input_df = pd.DataFrame([user_data])

    # Ensure that input_df has the same feature columns used in training (features_used)
    input_df = input_df.reindex(columns=features_used, fill_value=0)

    # Make prediction
    predicted_budget = model.predict(input_df)[0]
    print("Predicted weekly budget:", predicted_budget)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python budgtest.py <user_id>")
        sys.exit(1)

    user_id = int(sys.argv[1])
    main(user_id)