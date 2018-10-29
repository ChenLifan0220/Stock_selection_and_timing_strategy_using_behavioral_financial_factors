#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:18:05 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt

'''
close_price_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ100_all_close_price.csv",sep=",",index_col=0)
turnover_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_turnover_ratio.csv",sep=",",index_col=0)
deal_price_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_average_price.csv",sep=",",index_col=0)
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_return.csv",sep=",",index_col=0)

'''
close_price_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ500_all_close_price.csv",sep=",",index_col=0)
turnover_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_turnover_ratio.csv",sep=",",index_col=0)
deal_price_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_average_price.csv",sep=",",index_col=0)
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv",sep=",",index_col=0)


close_price_original=close_price_original.fillna('NaN')
turnover_original=turnover_original.fillna(value=0)
deal_price_original=deal_price_original.fillna(value=0)

##CGO measure
stock_code_list1=close_price_original.index.tolist()
stock_code_list2=turnover_original.index.tolist()
stock_code_list3=deal_price_original.index.tolist()
stock_code_list4=return_original.index.tolist()
stock_code_list5=[i for i in stock_code_list1 if i in stock_code_list2]
stock_code_list6=[i for i in stock_code_list3 if i in stock_code_list5]

#get the intersection of the three stock datasets
stock_code_list=[i for i in stock_code_list4 if i in stock_code_list6]

#get monthly_sequence and daily_sequence
monthly_sequence=return_original.columns.values.tolist()
daily_sequence=turnover_original.columns.values.tolist()
#daily_sequence=daily_sequence[200:]

#get sequence number of month in daily_sequence and ensure the number bigger than 200
#get new monthly sequence
sequence_number=[]
Monthly_sequence=[]
for no1 in range(len(monthly_sequence)):
    for no2 in range(len(daily_sequence)):
        if daily_sequence[no2]==monthly_sequence[no1]:
            if no2>200:
                sequence_number.append(no2)
                Monthly_sequence.append(monthly_sequence[no1])

#set the Average_price_100days index to related date
Average_price_100days=pd.DataFrame(index=Monthly_sequence)

#set the Reference_Price index to related date
Reference_Price=pd.DataFrame(index=Monthly_sequence)

#set the CGO_factors index to related date
CGO_factors=pd.DataFrame(index=Monthly_sequence)

for s in stock_code_list:
#for s in ['000001.SZ']:
    single_close_price=close_price_original.loc[s]
    single_turnover=turnover_original.loc[s]
    single_deal_price=deal_price_original.loc[s]
    
    Average_price=[]
    Reference_price=[]
    CGO_factor=[]
    
    #use  sliding window method to get CGO factor for each day (after 200th day)
    #for i in range(201,len(single_close_price)):
    for i in sequence_number:
        
        #get 100 average deal price for each day (after 100th day)
        single_deal_average=[]
        for j in range(i-100,i):
            single_deal_price_interval=single_deal_price.iloc[j-100:j]
            single_deal_average.append(float(single_deal_price_interval.mean()))
        Average_price.append(single_deal_average[-1])
        
        #get turnover ratio weight for each day (after 100th day)
        single_turnover_interval=single_turnover.iloc[i-100:i]
        turnover_weight=[]
        for k in range(0,99):
            turnover_weight_sub=single_turnover_interval.iloc[k]
            for l in range(k+1,100):
                turnover_weight_sub=turnover_weight_sub*(1-single_turnover_interval.iloc[l])
            turnover_weight.append(turnover_weight_sub)
        turnover_weight.append(single_turnover_interval.iloc[99])
        
        #standardize turnover ratio weight
        if sum(turnover_weight)!=0:
            turnover_weight_standared=[t/sum(turnover_weight) for t in turnover_weight]
        
        #calculate reference price
        reference_price=0
        for n in range(0,100):
            reference_price+=turnover_weight_standared[n]*single_deal_average[n]
#        for n in range(1,101):
#            reference_price+=turnover_weight_standared[n-1]*single_deal_average[-n]
        
        #get reference_price sequence
        Reference_price.append(reference_price)
        
        #calculate CGO factor
        #if single_close_price.iloc[i-1]!='NaN':
            #CGO_factor.append((single_close_price.iloc[i-1]-reference_price)/single_close_price.iloc[i-1])
        if reference_price!=0:
            CGO_factor.append((single_close_price.iloc[i-1]-reference_price)/reference_price)
        else:
            CGO_factor.append(np.nan)

    #get Reference price dataframe (whose index is monthly sequence, columns are stock name)
    single_Average_price=pd.DataFrame({s:Average_price},index=Monthly_sequence)
    Average_price_100days=pd.concat([Average_price_100days,single_Average_price],axis=1)
    
    #get Reference price dataframe (whose index is monthly sequence, columns are stock name)
    single_Reference_price=pd.DataFrame({s:Reference_price},index=Monthly_sequence)
    Reference_Price=pd.concat([Reference_Price,single_Reference_price],axis=1)
    
    #get CGO dataframe (whose index is monthly sequence, columns are stock name)
    single_CGO_factors=pd.DataFrame({s:CGO_factor},index=Monthly_sequence)
    CGO_factors=pd.concat([CGO_factors,single_CGO_factors],axis=1)

Close_price=close_price_original.loc[:,Monthly_sequence].T

Average_price_100days.to_csv("/Users/lilychen/Desktop/dissertation/Results/Average_price_100days_ZZ500.csv")
Reference_Price.to_csv("/Users/lilychen/Desktop/dissertation/Results/Reference_Price_ZZ500.csv")
CGO_factors.to_csv("/Users/lilychen/Desktop/dissertation/Results/CGO_factors_ZZ500.csv")
Close_price.to_csv("/Users/lilychen/Desktop/dissertation/Results/Close_price_ZZ500.csv")










 
        



