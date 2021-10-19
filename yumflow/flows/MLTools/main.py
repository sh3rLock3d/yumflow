import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from io import BytesIO
import requests


def read_CSV_data(csv_byte, labels):
    df = pd.read_csv(BytesIO(csv_byte))
    if (labels):
        now = pd.to_datetime("now")
        df['Time'] = [now for _ in range(len(df))]
    return df


def data_split(x, y, test_size):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    return x_train, x_test, y_train, y_test


def append_data(df1, df2):
    return df1.append(df2, ignore_index=True)


def show_digest_of_data(x):
    return x.head(5)


def instagram_accounts_exists(accounts):
    import requests
    notTaken = []
    for i in accounts:
        response = requests.get("https://instagram.com/" + i + "/")
        print(response)
        if response.status_code == 404:
            notTaken.append(i)
    return notTaken
