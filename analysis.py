import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('/home/alpaca/train.csv')
data_test = pd.read_csv('/home/alpaca/test.csv')

ex_train=list(set(data['device_ifa']))
n_train=len(list(set(data['device_ifa'])))
print('	device_ifa',ex_train)
print('	number of device_ifa is ',n_train)