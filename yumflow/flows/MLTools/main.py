import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from io import BytesIO
import requests


def read_CSV_data(csv_byte, labels):
    labels = ''.join(labels.split()).split(',')
    df = pd.read_csv(BytesIO(csv_byte))
    y = df[labels]
    x = df.loc[:, ~df.columns.isin(labels)]
    return x, y


def data_split(x, y, test_size):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    return x_train, x_test, y_train, y_test


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
