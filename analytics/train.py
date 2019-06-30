# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

train_data = pd.read_csv('analytics/data/train_data.csv')

target = train_data['like'].values
features = train_data[['cost', 'distance', 'score', 'tagId']].values

train_x, test_x, train_y, test_y = train_test_split(
    features, target, test_size=0.30, stratify=target, random_state=33)

# train
clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(train_x, train_y)

# test
acc_decision_tree = round(clf.score(test_x, test_y), 6)
print(u'score 准确率为 %.4lf' % acc_decision_tree)

joblib.dump(clf, 'analytics/data/train_model')
