# -*- coding: utf-8 -*-
"""DeepCTR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZyFPigYTOgi3A2yGO5vAKZzEkUAqHHG_
"""

#pip install -U deepctr-torch

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from deepctr_torch.models import DeepFM
from deepctr_torch.inputs import  SparseFeat, DenseFeat,get_feature_names

data = pd.read_csv('/content/drive/My Drive/20 20 ViSiON /IGAWorks/Data/train.csv')

data.head(25)

sparse_features = data.columns[1:]
# sparse_features
data[sparse_features] = data[sparse_features].fillna('-1', )
target = ['click']

for feat in sparse_features:
    lbe = LabelEncoder()
    data[feat] = lbe.fit_transform(data[feat])

fixlen_feature_columns = [SparseFeat(feat, data[feat].nunique())
                        for feat in sparse_features]

dnn_feature_columns =  fixlen_feature_columns
linear_feature_columns =  fixlen_feature_columns

feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

train, test = train_test_split(data, test_size=0.2)
train_model_input = {name:train[name] for name in feature_names}
test_model_input = {name:test[name] for name in feature_names}

device = 'cuda:0'
model = DeepFM(linear_feature_columns=linear_feature_columns, dnn_feature_columns=dnn_feature_columns, task='binary',
                   l2_reg_embedding=1e-5, device=device)

model.compile("adagrad", "binary_crossentropy",
                  metrics=["binary_crossentropy", "auc"],)
model.fit(train_model_input, train[target].values,
              batch_size=256, epochs=10, validation_split=0.2, verbose=2)

pred_ans = model.predict(test_model_input, 256)
