import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

import pickle

PATH = 'data/Crop_recommendation.csv'
df = pd.read_csv(PATH)

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
label = df['label']

# Splitting into train and test dataset
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

# randomForestClassifier
RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain, Ytrain)

# make predictions
predicted_values = RF.predict(Xtest)

# print classification report
# print(classification_report(Ytest,predicted_values))

# save trained RandomForest
RF_pkl_filename = 'models/RandomForest.pkl'
# Open the file to save as pkl file
RF_Model_pkl = open(RF_pkl_filename, 'wb')
pickle.dump(RF, RF_Model_pkl)
# Close the pickle instances
RF_Model_pkl.close()



# # making a prediction
# data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])
# prediction = RF.predict(data)
# print(prediction)


# # GET TOP 5 CROP RECOMMENDATION

# # Your data input for prediction
# data = np.array([[83, 45, 60, 28, 70.3, 7.0, 150.9]])

# # Get probabilities for each class
# probabilities = RF.predict_proba(data)

# # Get the indices of the classes sorted by probability in descending order
# top_5_indices = np.argsort(probabilities, axis=1)[:, ::-1][:, :5]

# # Get the corresponding class names for the top 5 indices
# top_5_crops = RF.classes_[top_5_indices]

# # Print the top 5 crop predictions
# print(top_5_crops)
