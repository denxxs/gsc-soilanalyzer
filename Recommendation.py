import pickle
import numpy as np

# Load the model from the .pkl file
with open('models/RandomForest.pkl', 'rb') as file:
    model = pickle.load(file)

# Example input data
data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])

# Make predictions using the loaded model
predicted_values = model.predict(data)

# Print the predictions
print(predicted_values)


# Your data input for prediction
data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])

# Get probabilities for each class
probabilities = model.predict_proba(data)

# Get the indices of the classes sorted by probability in descending order
top_5_indices = np.argsort(probabilities, axis=1)[:, ::-1][:, :5]

# Get the corresponding class names for the top 5 indices
top_5_crops = model.classes_[top_5_indices]

# Print the top 5 crop predictions
print(top_5_crops)
 