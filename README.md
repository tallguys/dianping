# dianping

这是一个通过深度学习了解你的个人喜好，自动报名大众点评霸王餐的脚本。

## Dependency
- python3
- scrapy
- scikit-learn

## Step

1. 用抓包工具获取大众点评app登录的用户信息，填写到环境变量或*config.py*

1. 通过爬虫获取训练集数据
    ```
    $ scrapy crawl list_free_meals
    ```

1. 给数据打标签并清理数据得到训练数据集 -> **analytics/data/train_data.csv**

1. 选择最优算法
    ```
    $ python3 analytics/data/choose_classifier.py
    ```

1. 执行以下命令得到训练模型 -> **analytics/data/train_model**
    ```
    $ python3 analytics/data/train.py
    ```

1. 执行以下命令查看预测结果是否符合预期 -> **analytics/data/predict.csv**
    ```
    $ python3 analytics/data/test.py
    ```

1. 根据训练结果报名霸王餐
    ```
    $ scrapy crawl apply_free_meals
    ```