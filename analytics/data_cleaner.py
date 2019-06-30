import pandas as pd
from sklearn.feature_extraction import DictVectorizer

result_data = pd.read_csv('analytics/data/tagged_data.csv')
origin_data = pd.read_csv('analytics/data/raw_data.csv')

dest_data: pd.DataFrame = origin_data.merge(on='id', right=result_data)

dest_data.drop(columns=['id', 'title_x', 'title_y', 'cost_y', 'shopAddress_y', 'distanceInfo_y',
                        'distance_y', 'score_y', 'shopName_x', 'shopName_y', 'tagId_y', 'tagName_y',
                        'shopAddress_x', 'distanceInfo_x', 'tagName_x', 'like_x'], inplace=True)

dest_data.rename(columns={
    'cost_x': 'cost',
    'distance_x': 'distance',
    'score_x': 'score',
    'tagId_x': 'tagId',
    'like_y': 'like',
}, inplace=True)

dest_data.to_csv('analytics/data/train_data.csv', index=False)
