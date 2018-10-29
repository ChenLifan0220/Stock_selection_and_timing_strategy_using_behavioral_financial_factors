#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:28:04 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt
from math import isnan
from sklearn import svm
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import RandomForestRegressor


CO_factors=pd.read_csv("/Users/lilychen/Desktop/dissertation/Results/CO_factors_ZZ500.csv",sep=",",index_col=0)
CGO_factors=pd.read_csv("/Users/lilychen/Desktop/dissertation/Results/CGO_factors_ZZ500.csv",sep=",",index_col=0)
return_original=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv",sep=",",index_col=0)
CO_factors=CO_factors.fillna(method='ffill',axis=0)
CGO_factors=CGO_factors.fillna(method='ffill',axis=0)
return_original=return_original.fillna(method='ffill',axis=0)
New_monthly_sequence=CO_factors.index.tolist()
Stock_list=CO_factors.columns.values.tolist()

def Removez_extremum(X):
    for s in Stock_list:
    #for s in ['000030.SZ']:
        a=X[s]
        aa=a.dropna().median()
        pb_MAD=a.apply(lambda x:abs(x-aa) if isnan(x)==False else np.nan)
        aaa=pb_MAD.dropna().median()
        b=aa+5*aaa
        c=aa-5*aaa
        a[a>b]=b;a[a<c]=c
        X[s]=a.apply(lambda x:(x - a.mean()) / a.std())
    return X

CO_factors=Removez_extremum(CO_factors)
CGO_factors=Removez_extremum(CGO_factors)
delta_CGO=CGO_factors-CGO_factors.shift(1,axis=0)

#CGO_factors.to_csv('/Users/lilychen/Desktop/dissertation/Results/CGO_factors_ZZ500_processed.csv')
#delta_CGO.to_csv('/Users/lilychen/Desktop/dissertation/Results/delta_CGO_factors_ZZ500_processed.csv')

CGO_factors=CGO_factors.loc[New_monthly_sequence]
delta_CGO=delta_CGO.loc[New_monthly_sequence]
return_original=return_original.T
New_monthly_sequence1=[str(x) for x in New_monthly_sequence]
return_original=return_original.loc[New_monthly_sequence1]
return_original.index=New_monthly_sequence

prediction=pd.DataFrame()
return_old=pd.DataFrame()
prediction_real_value=pd.DataFrame()

for s in Stock_list:
#for s in ['000005.SZ']:
    predict=[]
    predict_real_value=[]
    single_CO=CO_factors.loc[:,s]
    single_delta_CGO=delta_CGO.loc[:,s]
    single_return=return_original.loc[:,s]
    single_return=single_return.apply(lambda x:1 if x>=0 else -1)
    
    for d in range(len(New_monthly_sequence)-13):
        single_CO_train=single_CO.iloc[d:d+12]
        single_delta_CGO_train=single_delta_CGO.iloc[d:d+12]
        single_return_train=single_return.iloc[d:d+12]
        test1=single_CO.iloc[d+13]
        test2=single_delta_CGO.iloc[d+13]
        train=pd.concat([single_CO_train,single_delta_CGO_train],axis=1)
        test=[test1,test2]
        clf=svm.SVR()
        #clf=RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
        #regr=RandomForestRegressor(n_estimators=50, max_depth=2,random_state=0)
        if (single_CO_train.isnull().values.any()==False)&(single_delta_CGO_train.isnull().values.any()==False):
            if isnan(test1)==False:
                clf.fit(train,single_return_train)
                predict_real_value.append(clf.predict([test]))
                if clf.predict([test])>=0:
                    predict.append(1)
                else:
                    predict.append(-1)
            else:
                predict.append(np.nan)
        else:
            predict_real_value.append(np.nan)
            predict.append(np.nan)
            
    single_prediction=pd.DataFrame({s:predict},index=New_monthly_sequence[13:])
    prediction=pd.concat([prediction,single_prediction],axis=1)
    return_old=pd.concat([return_old,single_return[13:]],axis=1)
    single_predict_real_value=pd.DataFrame({s:predict_real_value},index=New_monthly_sequence[13:])
    prediction_real_value=pd.concat([prediction_real_value,single_predict_real_value],axis=1)

prediction.to_csv("/Users/lilychen/Desktop/dissertation/Results/randomforestregression_prediction_result.csv")
#return_old.to_csv("/Users/lilychen/Desktop/dissertation/Results/result_original.csv")
prediction_real_value.to_csv("/Users/lilychen/Desktop/dissertation/Results/STF_prediction.csv")

#test accuracy
count=0
nan_count=0
for i in range(len(single_prediction)):
    for j in range(len(Stock_list)):
        if isnan(prediction.iloc[i,j])==False&isnan(return_old.iloc[i,j]==False):
            if prediction.iloc[i,j]*return_old.iloc[i,j]>=0:
                count+=1
        else:
            nan_count+=1
print(count/(len(single_prediction)*len(Stock_list)-nan_count))


prediction_result=pd.DataFrame()
for s in Stock_list:
    stock_prediction=[]
    for i in range(len(single_prediction)):
        if isnan(prediction.iloc[i,j])==False&isnan(return_old.iloc[i,j]==False):
            if prediction.iloc[i,j]*return_old.iloc[i,j]>=0:
                stock_prediction.append(1)
            else:
                stock_prediction.append(-1)
        else:
            stock_prediction.append(np.nan)
    single_prediction_result=pd.DataFrame({s:stock_prediction},index=New_monthly_sequence[13:])
    prediction_result=pd.concat([prediction_result,single_prediction_result],axis=1)


'''
train_data_index=New_monthly_sequence[:int(len(New_monthly_sequence)*(12/126))]
test_data_index=New_monthly_sequence[int(len(New_monthly_sequence)*0.75):]

#get CO (variable x1) dataset
train_data_CO=CO_factors.loc[train_data_index]
#train_data_CO=train_data_CO.apply(lambda x: x)
test_data_CO=CO_factors.loc[test_data_index]

#get CGO (variable x2) dataset
train_data_CGO=delta_CGO.loc[train_data_index]
test_data_CGO=CGO_factors.loc[test_data_index]

#get return (varialble y) dataset
train_data_return=return_original.loc[train_data_index]
test_data_return=return_original.loc[test_data_index]


#get coefficient
data1={'CO':train_data_CO, 'delta_CGO':train_data_CGO, 'returns':train_data_return}
train_data=pd.Panel(data1).to_frame()
train_data['returns']=train_data['returns'].apply(lambda x:1 if x>0 else -1)
train_data.to_csv("/Users/lilychen/Desktop/dissertation/Results/train_result.csv")
'''



