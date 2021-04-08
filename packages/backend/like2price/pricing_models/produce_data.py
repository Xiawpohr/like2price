
import pandas as pd
import random

from django.conf import settings

DATA_NUM = 1000
BASE_ETH_PRICE = 0.01
LOW_ETH_PRICE = 0.01
HIGH_ETH_PRICE = 10.5
LOW_LIKE_NUMBER = 0
HIGH_LIKE_NUMBER = 30000

#####
# columns no, price, feature1_likes, feature2_dislikes, feature3_followers
####

col_names = [
    'No',
    'Price',
    'Feature1_likes',
    'Feature2_dislikes',
    'Feature3_followers',
]

absolute_path = settings.BASE_DIR


def produce_data():
    lines = []
    for d_num in range(0, DATA_NUM):
        likes = random.randint(LOW_LIKE_NUMBER, HIGH_LIKE_NUMBER)
        dislikes = random.randint(LOW_LIKE_NUMBER, HIGH_LIKE_NUMBER)
        followers = random.randint(LOW_LIKE_NUMBER, HIGH_LIKE_NUMBER)
        total = likes*(1/3) + dislikes*(-1/3) + followers*(1/3)
        total = 0 if total < 0 else total
        price = total * (HIGH_ETH_PRICE - LOW_ETH_PRICE) / \
            HIGH_LIKE_NUMBER + BASE_ETH_PRICE
        lines.append((d_num, price, likes, dislikes, followers))
    df = pd.DataFrame(lines, columns=col_names)
    df.to_csv(f'{absolute_path}/pricing_models/data/data.csv',
              index=False, header=col_names)


if __name__ == "__main__":
    produce_data()
