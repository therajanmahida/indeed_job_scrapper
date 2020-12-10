from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
import numpy as np
from scipy import sparse
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump, load

def import_data():
    X_train_vec = sparse.load_npz('data\X_train_vec.npz')
    X_test_vec = sparse.load_npz('data\X_test_vec.npz')
    y_train_vec = np.load('data\y_train_vec.npy')
    y_test_vec = np.load('data\y_test_vec.npy')
    return (X_train_vec, y_train_vec, X_test_vec, y_test_vec)


if __name__ == "__main__":
    X_train_vec, y_train_vec, X_test_vec, y_test_vec = import_data()
    

    # define models
    KNN_classifier=KNeighborsClassifier(n_neighbors=11, weights='distance') #0.885
    LREG_classifier=LogisticRegression(solver='liblinear', C=0.1, penalty='l2')
    DT_classifier = DecisionTreeClassifier(criterion='entropy', max_depth=12)
    MLP_classifier = MLPClassifier(max_iter=50, activation='relu', learning_rate_init=0.0001, solver='adam')
    SVC_classifier = SVC(C=0.5, gamma='scale')
    NB_classifier = GaussianNB(var_smoothing=1e-8)


    predictors_all = [('KNN',KNN_classifier),('LREG',LREG_classifier),('DT',DT_classifier), ('MLP', MLP_classifier), ('SVC', SVC_classifier), ('GNB', NB_classifier)]
    predictors_top3 = [('LREG',LREG_classifier), ('MLP', MLP_classifier), ('SVC', SVC_classifier)]
    
    # choose the set of predictors you want to use from the list above
    VT=VotingClassifier(predictors_top3, verbose=True)

    #train all classifier on the same datasets
    VT.fit(X_train_vec,y_train_vec)


    trained_model = dump(VT, 'trained_model.joblib')
    #use hard voting to predict (majority voting)
    pred=VT.predict(X_test_vec)

    #print accuracy
    print("The accruacy of the enssemble is:", accuracy_score(y_test_vec, pred))
    print("\nThe Confusion Matrix of the Ensemmble is:\n", confusion_matrix(y_test_vec, pred))