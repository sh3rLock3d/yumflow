from cmath import nan
import re
from telnetlib import PRAGMA_HEARTBEAT
from django.db.models import query
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from io import BytesIO
import torch
from torch import mode, ne, nn
from torch.utils.data import TensorDataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from .enums import *
from .network import *

from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def read_CSV_data(csv_byte, labels):
    df = pd.read_csv(BytesIO(csv_byte) ,)

    if (labels):
        now = pd.to_datetime("now")
        df['Time'] = [now for _ in range(len(df))]
    return df


def data_split(x, y, test_size):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    return x_train, x_test, y_train, y_test


def get_data_x_and_y(df, label):
    cols = list(df.columns)
    cols.remove(label)
    return df[cols].to_numpy(), df[[label]].to_numpy()


def append_data(df1, df2):
    return df1.append(df2, ignore_index=True)


def show_digest_of_data(x):
    shape = x.shape
    x = x.fillna('')
    header = list(x.columns)
    if len(header) >= 10:
        header = header[:5] + ['...'] + header[-5:]
    index = list(x.index.values) 
    if len(header) >= 10:
        index = index[:5] + ['...'] + index[-5:]
    data = []
    for c in header:
        temp = []
        for r in index:
            if c== '...' or r =='...':
                temp.append('...')
            else:
                temp.append(x.at[r,c])
        data.append(temp)
    shape = x.shape


    return {'header':header, 'index':index, 'data':data, 'shape':shape}

def get_data_info(df):
    colType = []
    colName = []
    for name, type in df.dtypes.items():
        colName.append(name)
        colType.append(str(type))

    a = {"shape":df.shape, 'columnsName':colName, 'colType':colType}
    return a

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
    

    if constraints != "[]" and constraints != "":
        df = df.query(constraints)
    
    
    return df

def prepare_train_and_test_by_prepration(cols, colFilter, constraints,nans, categories, normalize, sliceStr ,train, test):
    train = filter_data(cols, colFilter, constraints, train)
    test = filter_data(cols, colFilter, constraints, test)
    # nans    
    try:
        for c in nans:
            median = train[c].median()
            train[c].fillna(median, inplace=True)
            test[c].fillna(median, inplace=True)
    except:
        raise Exception("در ورودی ها ی پر کردن سطر های خالی زیر با میانگین مشکلی وجود دارد.")
    # sliceStr
    
    try:
        for c in sliceStr:
            test[c] = test[c].str.slice(0, 1)
            train[c] = train[c].str.slice(0, 1)
    except:
        raise Exception("در ورودی ها ی گرفتن حرف اول سطر ستون ها مشکلی وجود دارد.")
    #categories
    try:
        categorical_cols = categories
        train = pd.get_dummies(train,columns=categorical_cols, prefix=categorical_cols, dummy_na=True)

        test = pd.get_dummies(test, columns=categorical_cols, prefix=categorical_cols, dummy_na=True)
    except:
        raise Exception("در ورودی ها ی سطر های کتگوری مشکلی وجود دارد.")
    
    
    #normalize
    try:
        to_normalize = normalize
        for each in to_normalize:
            mean, std = train[each].mean(), train[each].std()
            train.loc[:, each] = (train[each] - mean) / std
            test.loc[:, each] = (test[each] - mean) / std
    except:
        raise Exception("در ورودی ها ی سطر های نرمالایز مشکلی وجود دارد.")
    
    cols_must_be_in_train = [i for i in test.columns if i not in train.columns]
    cols_must_be_in_test = [i for i in train.columns if i not in test.columns]
    for i in cols_must_be_in_train:
        train[i] = np.zeros(train.shape[0])
    for i in cols_must_be_in_test:
        test[i] = np.zeros(test.shape[0])
    test = test[train.columns]
    return train, test




def createNet(layer):
    net = create_network(layer)
    file_name = 'flows/MLTools/model.pth'
    torch.save(net.state_dict(), file_name)
    return net

def loadModel(path, layer):   
    model = create_network(layer)
    model.load_state_dict(torch.load(path))
    return model

def train_network(train_info, net, x_train, y_train):
    model, result = train_the_network(train_info, net, x_train, y_train)
    file_name = 'flows/MLTools/model.pth'
    torch.save(model.state_dict(), file_name)
    return model, result

def test_model(info, model, x_test, y_test):
    return test_network(info, model, x_test, y_test)