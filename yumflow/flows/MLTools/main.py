from django.db.models import query
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from io import BytesIO

from .createModel.main_insta import Create
from .createModel.set_config import SetConfig



def read_CSV_data(csv_byte, labels):
    df = pd.read_csv(BytesIO(csv_byte) , delimiter = "|")
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

def create_query(constraints):
    query = []
    for constraint in constraints:
        temp = ""
        if constraint[1]:
            temp += 'not '
        temp += '( '
        col = constraint[0]
        row_query = []
        for i in constraint[2]:
            temp1 = '( '
            if i[0] == '==':
                temp1 += col + ' == ' + i[1]
            elif i[0] == "<":
                temp1 += col + ' < ' + i[1]
            elif i[0] == ">":
                temp1 += col + ' > ' + i[1]
            elif i[0] == "!=":
                temp1 += col + ' != ' + i[1]
            elif i[0] == "isin":
                x = [x.strip() for x in i[1].split(',')]
                x = str(x)
                temp1 += col + ' in [ ' + i[1] + ' ]'
            elif i[0] == "~isin":
                x = [x.strip() for x in i[1].split(',')]
                x = str(x)
                temp1 += col + ' not in [ ' + i[1] + ' ]'
            temp1 += ' ) '
            row_query.append(temp1)
        temp += " or ".join(row_query) + ") "
        query.append(temp)
    query = "and ".join(query)
    return query


def filter_data(cols, colFilter, constraints, df):
    df = df
    # col
    if colFilter == 1:
        df = df.loc[:, ~df.columns.isin(cols)]
    elif colFilter == 2:
        df = df[cols]
    if constraints:
        df = df.query(constraints)
    file_name = 'flows/MLTools/createModel/train.csv'
    df.to_csv(file_name, sep='|', encoding='utf-8')
    a = SetConfig(True)
    b = Create()

def test_data(df):
    file_name = 'flows/MLTools/createModel/test.csv'
    df.to_csv(file_name, sep='|', encoding='utf-8')
    a = SetConfig(False)
    b = Create()
    return b