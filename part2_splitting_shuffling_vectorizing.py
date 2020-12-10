import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
from scipy import sparse
import os
from joblib import dump, load



def load_data(data_path):
    alldata_df = pd.read_csv(data_path) 
    alldata_df.columns = ['Text', 'Job_Title']
    all_X = alldata_df['Text']
    all_y = alldata_df['Job_Title']
    print("data is stored into X and y")
    #remove label names from descriptions
    all_X = all_X.str.replace('data sci[a-z]+', '', regex = True, case=False)
    all_X = all_X.str.replace('data eng[a-z]+', '', regex = True, case=False)
    all_X = all_X.str.replace('software eng[a-z]+', '', regex = True, case=False)
    return(all_X, all_y)



def vectorize_training_data(X_train, X_test):
    #Build a counter based on the training dataset
    counter = CountVectorizer()
    counter.fit(X_train)
    #count the number of times each term appears in a document and transform each doc into a count vector
    fitted_counter = dump(counter, "fitted_counter.joblib")
    X_train_vec = counter.transform(X_train)#transform the training data
    X_test_vec = counter.transform(X_test)#transform the testing data
    return X_train_vec, X_test_vec



def vectorize_labels(y_train, y_test):
    y_train_vec = []
    for row in y_train:
        if row == "data engineer":
            y_train_vec.append(0)
        elif row == "data scientist":
            y_train_vec.append(1)
        elif row == "software engineer":
            y_train_vec.append(2)
    y_test_vec = []
    for row in y_test:
        if row == "data engineer":
            y_test_vec.append(0)
        elif row == "data scientist":
            y_test_vec.append(1)
        elif row == "software engineer":
            y_test_vec.append(2)
    return(y_train_vec, y_test_vec)



if __name__ == "__main__":
    #Load the data
    all_X, all_y = load_data("ads_combined.csv")
    all_X.to_csv("all_X_after_replacement.csv")
    #Split the data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y, test_size=0.10, random_state=123)
    #Vectorizing the job descriptions: turning words of the job description into vectors do the classifier can do work on it
    X_train_vec, X_test_vec = vectorize_training_data(X_train, X_test)
    #Vectorize the labels: words into 0 or 1 or 2
    y_train_vec, y_test_vec = vectorize_labels(y_train, y_test)
    # training and test data and labels (everything) is in vectors (numbers) --ready to train a model

    current_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(current_dir, str("data/"))):
        os.makedirs(os.path.join(current_dir, str("data/")))
    sparse.save_npz("data/X_train_vec.npz", X_train_vec)
    sparse.save_npz("data/X_test_vec.npz", X_test_vec)
    np.save("data/y_train_vec.npy", y_train_vec)
    np.save("data/y_test_vec.npy", y_test_vec)





