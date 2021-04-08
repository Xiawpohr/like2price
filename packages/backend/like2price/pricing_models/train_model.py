import os
import pandas as pd
import numpy as np
from typing import List
from numbers import Number
from sklearn.linear_model import LinearRegression

from django.conf import settings

absolute_path = settings.BASE_DIR


def predict(likes: Number, dislikes: Number, followers: Number) -> Number:
    filepath = f'{absolute_path}/pricing_models/data/data.csv'
    newdata_filepath = f'{absolute_path}/pricing_models/data/data_new.csv'
    if os.path.islink(newdata_filepath):
        df = pd.read_csv(newdata_filepath)
    else:
        df = pd.read_csv(filepath)
    x = np.array(
        df[["Feature1_likes", "Feature2_dislikes", "Feature3_followers"]])
    y = np.array(df[["Price"]])
    lm = LinearRegression()
    lm.fit(x, y)

    # to predict likes2price
    to_be_predicted = np.array([
        [likes, dislikes, followers]
    ])
    predicted_price = lm.predict(to_be_predicted)[0][0]

    # prediction result
    return 0 if predicted_price < 0 else predicted_price


def re_train_model(data: List[List]):
    """
        List[data]: [Price, Feature1_likes, Feature2_dislikes, Feature3_followers]
    """
    filepath = f'{absolute_path}/pricing_models/data/data.csv'
    newdata_filepath = f'{absolute_path}/pricing_models/data/data_new.csv'
    df = pd.read_csv(filepath)
    col_names = df.columns
    lines_number = df[df.columns[0]].count()
    lines = []
    for i, d in enumerate(data):
        if len(d) != 4:
            continue
        lines.append((lines_number, d[0], d[1], d[2], d[3]))
        lines_number += 1

    df_new = pd.DataFrame(lines, columns=col_names)
    df = pd.concat([df, df_new])

    df.to_csv(newdata_filepath, index=False, header=col_names)


if __name__ == "__main__":
    print(predict(10000, 500, 10000))

    # re_train_model([[2, 1, 2, 3]])
