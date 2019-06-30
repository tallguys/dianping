import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

MODEL = 'analytics/data/train_model'


def predict(features):
    clf: DecisionTreeClassifier = joblib.load(MODEL)
    return clf.predict([
        [
            features['cost'],
            features['distance'],
            features['score'],
            features['tagId']
        ]
    ])[0]
