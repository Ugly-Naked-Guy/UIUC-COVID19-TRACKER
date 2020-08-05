import csv
import os
import pandas as pd
import numpy as np
import hashdate as hd

abspath = os.path.dirname(os.path.abspath(__file__))

## read the joined user & reported table:
df_user = pd.read_csv(open(abspath + '/static/user.csv'))

df_reported = pd.read_csv(open(abspath + '/static/reported.csv'))

df_merge = pd.merge(df_user, df_reported, how='right', on=['userID'])

symptoms_list = ['Cough', 'Headache', 'Diarrhea', 'Fatigue', 'Shortness of Breath', 'Chills', 'Conjunctivitis',
                 'Sore Throat', 'Chest Pain']
location_list = ['Grainger Library', 'Illini Union', 'ECE building', 'Illini Hall', 'Bookstore',
                 'Altgeld Hall']

original_csv_list = ['/static/Grainger_Library.csv', '/static/Illini_Union.csv', '/static/ECE_building.csv', '/static/Illini_Hall.csv', '/static/Bookstore.csv',
                     '/static/Altgeld_Hall.csv']

## make dummy variables:
for symptoms in symptoms_list:
    df_merge[symptoms] = list(map(lambda x: 1 if symptoms in x else 0, df_merge['symptoms']))

df_dummies = df_merge.join(pd.get_dummies(df_merge.placesVisited)).join(pd.get_dummies(df_merge.testResult)).join(
    pd.get_dummies(df_merge.gender))
cols_to_drop = ['placesVisited', 'testResult', 'symptoms', 'gender', 'Female', 'Unknown', 'Negative', 'healthState',
                'userName', 'password', 'department', 'address', ]
df_training = df_dummies.drop(cols_to_drop, axis=1)

## update the weights for locations based on date and confirmed cases:
# calculate the weights2(backsum) using hash table
for i in range(len(location_list)):
    location = location_list[i]
    original_csv = original_csv_list[i]
    df = df_training[(df_training[location] == 1) & (df_training['Positive'] == 1)][['reportDate', 'userID']]
    df.to_csv(abspath + original_csv)

for i in range(len(original_csv_list)):

    original_csv = original_csv_list[i]
    location = location_list[i]
    date_list = sorted(pd.read_csv(open(abspath + original_csv)).iloc[:, 1].unique())

    with open(original_csv, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    del data[0]
    ahd = []
    aho = []
    data.sort(key=lambda x: x[1])

    for i in range(0, len(data)):
        ahd.append((data[i][1], data[i][2]))
    # print('ahd:')
    # print(ahd)
    ahh = hd.hashdate(365, 20200101)
    for i in range(0, len(ahd)):
        ahh.insert(ahd[i][0], ahd[i][1])
    print('ahh:')
    # ahh.display()
    for i in range(0, len(ahh.t)):
        if ahh.t[i] != None:
            aho.append((ahh.outd(i), ahh.outn(i)))
            # print(ahh.outd(i))
    # print('aho:')
    # print(aho)

    weights_matrix2 = np.zeros(shape=(len(date_list), 6))
    for j in range(len(location_list)):
        for i in range(len(date_list)):
            date = date_list[i]
            weights_matrix2[i, j] = ahh.backsum(date)

# calculate the weights1(today)
dates_list = df_training["reportDate"].unique()
dates_df = pd.DataFrame(sorted(dates_list))
weights_matrix = np.zeros(shape=(len(dates_list), 6))

for i in range(len(dates_list)):
    date = dates_list[i]
    high_risk_df = df_training[(df_training['reportDate'] == date) & (df_training['Positive'] == 1)]
    risk_rate_raw = high_risk_df.sum(axis=0) / high_risk_df.shape[0]
    risk_rate = np.array(risk_rate_raw)[13:19]
    weights_matrix[i, :] = risk_rate

# weights_df = pd.DataFrame(weights_matrix*10)

weights_df = pd.DataFrame(weights_matrix * weights_matrix2)

df_dates_weights = pd.concat([dates_df, weights_df], axis=1)
df_dates_weights.columns = ['reportDate', 'Altgeld Hall', 'Bookstore', 'ECE building', 'Grainger Library',
                            'Illini Hall', 'Illini Union']
original_dates_df = pd.DataFrame(df_training[['reportDate']])
values_df = pd.merge(df_dates_weights, original_dates_df, how='left', on=['reportDate'])
values_matrix = np.array(values_df[location_list])
position_matrix = np.array(df_training[location_list])
weights_matrix = values_matrix * position_matrix

location_weights_df = pd.concat([pd.DataFrame(weights_matrix), original_dates_df], axis=1)
location_weights_df.columns = [location_list + ['reportDate']]

df_training_weights_merge = pd.concat([df_training.drop(location_list, axis=1), location_weights_df], axis=1)
df_training_weights = df_training_weights_merge.iloc[:, :-1].drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)

## save the training data to csv file
df_training_weights.to_csv(abspath + '/static/df_training_weights.csv')
