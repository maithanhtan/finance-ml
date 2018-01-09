mport numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
import matplotlib
matplotlib.use('TkAgg')
import math
import matplotlib.pyplot as plt 
import datetime
from matplotlib import style
import tkinter
import warnings
import os, os.path

dname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dname)

warnings.filterwarnings("ignore")

'''
import quandl
import pandas as pd
import json
import string
import os, os.path
quandl.ApiConfig.api_key = 'yvR18HYhyiyR51fL9UM5'
dname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dname)

codes_list_file = pd.read_csv("WIKI-datasets-codes.csv",names=["Code","Name"])

for exchange in codes_list_file['Code']:
	df = quandl.get(exchange)
	exchange1 = exchange.replace('/','-',1)
	file_path =  'data_files/' + exchange1 + '.csv' 
	
	df.to_csv(file_path)
	print(exchange+" - pulled")

'''

df = pd.read_csv('data_files/WIKI-AAPL.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
#preprocessing the data
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
#measure of volatility
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
first_for_compare = df['Adj. Close'].iloc[-1]

print(df.tail())
df.dropna(inplace=True)
y = np.array(df['label'])
print(first_for_compare)

num_instances = len(X)

seed = 7
num_samples = 10
test_size = 0.33
#kfold = model_selection.KFold(n_splits=5, random_state=seed)
kfold = model_selection.ShuffleSplit(n_splits=5, test_size=test_size, random_state=seed)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf2 = MLPRegressor()

confidence2kfold = model_selection.cross_val_score(clf2, X, y, cv=kfold)
print("MLP (KFold) : %.3f%% (%.3f%%)" % (confidence2kfold.mean()*100.0, confidence2kfold.std()*100.0))

clf2.fit(X_train, y_train)
confidence2 = clf2.score(X_test, y_test)
print("MLP : %.3f%%" % (confidence2*100.0))