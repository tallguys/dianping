# -*- coding: utf-8 -*-

import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

test_data = pd.read_csv('analytics/data/test_data.csv')

features = test_data[['cost', 'distance', 'score', 'tagId']].values

clf: DecisionTreeClassifier = joblib.load('analytics/data/train_model')
test_result = clf.predict(features)

test_data['like'] = test_result

test_data.to_csv('predict.csv')
