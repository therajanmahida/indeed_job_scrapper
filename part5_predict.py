import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
from joblib import dump, load
import csv

def load_data(data_path):
    alldata_df = pd.read_csv(data_path) 
    alldata_df.columns = ['Text']
    all_X = alldata_df['Text']
    print("data is stored into X")
    #remove label names from descriptions
    all_X = all_X.str.replace('data sci[a-z]+', '', regex = True, case=False)
    all_X = all_X.str.replace('data eng[a-z]+', '', regex = True, case=False)
    all_X = all_X.str.replace('software eng[a-z]+', '', regex = True, case=False)
    return(all_X)


def vectorize_data(all_X, counter_path):
    #Build a counter based on the training dataset
    counter = load(counter_path)
    #count the number of times each term appears in a document and transform each doc into a count vector
    X_vec = counter.transform(all_X)#transform the training data
    return X_vec


if __name__ == "__main__":
    # load the new data (no labels)
    all_X = load_data("test_data-allDE.csv")
    # use the existing vectorizer we fitted during training to vectorize the new data
    X_vec = vectorize_data(all_X, "fitted_counter.joblib")
    print("data is loaded and vectorized")
    
    # load the model we trained
    VT = load("trained_model.joblib")
    print("VC model loaded sucessfully")

    print("...initializing predictions")
    pred=VT.predict(X_vec)

    print("\n The predictions for the loaded data are\n", pred)
    
    output = open( 'output.csv', 'w', encoding='UTF-8' )
    writer = csv.writer( output, lineterminator='\n' )
    writer.writerow(['predictions'])
    for prediction in pred:
        writer.writerow([prediction])

    print("predictions saved to output.csv")
