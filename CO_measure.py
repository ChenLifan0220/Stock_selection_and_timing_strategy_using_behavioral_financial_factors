#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 21:30:37 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt
'''
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_return.csv",sep=",",index_col=0)
volume_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_volume.csv",sep=",",index_col=0)
monthly_sequence=return_original.columns.values.tolist()

'''
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv",sep=",",index_col=0)
volume_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_volume.csv",sep=",",index_col=0)
monthly_sequence=return_original.columns.values.tolist()


##CO measure
stock_code_list1=return_original.index.tolist()
stock_code_list2=volume_original.index.tolist()
stock_code_list=[i for i in stock_code_list1 if i in stock_code_list2]

CO_factors=pd.DataFrame(index=monthly_sequence[12:])
CO_accuracy=[]

for s in stock_code_list:
    ##取single stock的return and volume
    single_return=return_original.loc[s]
    single_volume=volume_original.loc[s]
    signed_volume=[]
    
    #get signed trading volume
    for i in range(len(single_volume)):
        if(single_return.iloc[i]<0):
            signed_volume.append(-single_volume.iloc[i])
        else:
            signed_volume.append(single_volume.iloc[i])
    signed_volume=pd.Series(signed_volume,name=s)
    
    #get CO factor
    co=[]
    
    for i in range(len(single_volume)-12):
        volume_interval=single_volume.iloc[i:i+12]
        standared_mean=float(volume_interval.sum())
        weighted_SV=0
        for j in range(11):
            weighted_SV+=signed_volume.iloc[i+j]*(j+1)
        if standared_mean!=0:
            co.append(weighted_SV/standared_mean)
        else:
            co.append(np.nan)
    
    CO_factor=pd.Series(co,name=s,index=monthly_sequence[12:])    
    CO_factors=pd.concat([CO_factors,CO_factor],axis=1)
    
    ##test accuracy
    real_performance=single_return.iloc[12:]
    real_performance=real_performance.fillna('NaN')
    CO_factor=CO_factor.fillna('NaN')
    predict_performance=[]
    
    for i in range(len(CO_factor)):
        if(real_performance.iloc[i]!='NaN')&(CO_factor.iloc[i]!='NaN'):
            if(real_performance.iloc[i]*CO_factor.iloc[i]>=0):
                predict_performance.append(1)
            else:
                predict_performance.append(0)
    
    predict_performance=pd.Series(predict_performance)

    if predict_performance.count():
        CO_accuracy.append(1-predict_performance.value_counts().loc[0]/predict_performance.count())
        
print(sum(CO_accuracy)/float(len(CO_accuracy)))
CO_factors.to_csv("/Users/lilychen/Desktop/dissertation/Results/CO_factors_ZZ500.csv")




