import numpy as np
import pandas as pd
import os


def sigmoid(z):
    a = 1/(1+np.exp(-z))
    return a


def initialize_with_zeros(X): # X is the model matrix
    w = np.zeros((X.shape[1], 1)) # dimision: p*1
    b = 0 # dimision: 1
    return w, b


def propagate(w, b, X, y):
    """
    pars:
    w -- weights, dimision: p*1
    b -- bias, dimision: 1
    X -- training dataset，dimision: n*p
    y -- true lables，dimision: p*1

    return:
    loss, dw, db, last two are put into the same dictionary gradients
    """
    # p = the number of columns in data matrix X
    p = X.shape[1]

    # forward propagatiion:
    A = sigmoid(np.dot(X, w)+b)  # using sigmoid function
    loss = -(np.sum(y*np.log(A)+(1-y)*np.log(1-A)))/p # the loss function of logistic regression

    # backward propagatiion：
    dZ = A-y
    dw = ((np.dot(dZ.T, X))/p).reshape(-1, 1)
    db = (np.sum(dZ))/p

    # retun：
    gradients = {"dw": dw,
                 "db": db}

    return gradients, loss


def optimize(w, b, X, y, num_iterations, learning_rate):
    # list to put loss after each iteration：
    loss_list = []
    # iteration：
    for i in range(num_iterations):
        # calulate loss and gradients after each iteration：
        gradients, loss = propagate(w, b, X, y)
        dw = gradients["dw"]
        db = gradients["db"]

        # update parameters w and b using the gradients:
        w = w - learning_rate*dw
        b = b - learning_rate*db

        # save the loss after per 100 iterations
        if i % 100 == 0:
            loss_list.append(loss)

    params = {"w": w,
              "b": b}
    gradients = {"dw": dw,
             "db": db}
    return params, gradients, loss_list


def Logistic_Regression(X, y, learning_rate=0.00001, num_iterations=1000):
    # get dimisions of the training data，intialize w and b：
    w, b = initialize_with_zeros(X)

    # gradient decent-calculate w and b through iterations
    params, gradients, loss_list = optimize(w, b, X, y, num_iterations, learning_rate)
    W = params['w']
    b = params['b']
#     proba = sigmoid(np.dot(new_record,W)+b)[0]
    pars = {"w": W,
            "b": b}
    return pars

def predict_user_posprob(userID):
    user_record = df_training_weights[df_training_weights["userID"] == userID].sort_values(
        'reportDate', ascending=False).iloc[0, :].drop(["userID", "reportDate", 'Positive', 'Unnamed: 0', 'Unnamed: 0.1'])
    print(user_record)
    user_to_predict = pd.DataFrame(user_record).T
    print(user_to_predict)
    proba = sigmoid(np.dot(user_to_predict, optimal_w)+optimal_b)[0][0]
    return proba

def find_location_weight(location_input, date_input):
    abspath = os.path.dirname(os.path.abspath(__file__))
    df_training = pd.read_csv(abspath + "/static/df_training.csv")
    high_risk_df = df_training[(df_training['reportDate'] == date_input) & (
        df_training['Positive'] == 1)]
    risk_rate_raw = high_risk_df.sum(axis=0)/high_risk_df.shape[0]
    risk_rate = np.array(risk_rate_raw)[13:19]

    dates_list = df_training["reportDate"].unique()

    if date_input in dates_list:
        return risk_rate * location_input * 10
    else:
        return location_input
