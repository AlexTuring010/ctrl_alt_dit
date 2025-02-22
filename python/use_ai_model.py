import pickle
import transflow as tf

# Load the model from the .pkl file
with open('./../models/xgb_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Example input data for prediction
input_data = tf.Tensor([1.0, 2.0, 3.0])  # Replace with your actual input data

# Use the model to make predictions
predictions = model.predict(input_data)

print(predictions)