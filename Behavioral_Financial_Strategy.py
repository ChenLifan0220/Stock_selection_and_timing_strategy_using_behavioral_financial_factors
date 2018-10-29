#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 22:57:19 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt

'''
CGO_factors=pd.read_csv('/Users/lilychen/Desktop/dissertation/Results/CGO_factors_ZZ100.csv',sep=",",index_col=0)
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_return.csv",sep=",",index_col=0)
Capital_factor = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/ZZ100_all_capital.csv",sep=",",index_col=0)
Volatility_monthly_factor = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/ZZ100_all_volatility.csv",sep=",",index_col=0)
'''

CGO_factors=pd.read_csv('/Users/lilychen/Desktop/dissertation/Results/CGO_factors_ZZ500.csv',sep=",",index_col=0)
return_original = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv",sep=",",index_col=0)
Capital_factor = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/ZZ500_all_capital.csv",sep=",",index_col=0)
Volatility_monthly_factor = pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/ZZ500_all_volatility.csv",sep=",",index_col=0)


stock_code_list=CGO_factors.columns.values.tolist()
monthly_sequence=CGO_factors.index.tolist()

Selected_stocks_monthly=pd.DataFrame()
for m in monthly_sequence:
#for m in [20071130]:
    #divide stocks according to CGO_factor value monthly
    group_A=[]
    group_B=[]
    
    single_month_CGOs=CGO_factors.loc[m]
    for i in range(len(single_month_CGOs)):
        if single_month_CGOs.iloc[i]>0:
            group_A.append(stock_code_list[i])
        else:
            group_B.append(stock_code_list[i])

    #select stocks in each group according to diffenrent factor
    #Volatility_monthly_factor select stocks for Group_A
    Group_A=(Volatility_monthly_factor.loc[group_A])[[str(m)]]
    Group_A=Group_A.dropna().sort_values([str(m)])
    
    #CGO_factor select stocks for Group_A
    #Group_A=single_month_CGOs.loc[group_A]
    #Group_A=Group_A.dropna().sort_values()
    
    #Capital_factor select stocks for Group_B
    #Group_B=(Capital_factor.loc[group_B])[[str(m)]]
    #Group_B=Group_B.dropna().sort_values([str(m)])
    
    #CGO_factor select stocks for Group_B
    #Group_B=single_month_CGOs.loc[group_B]
    #Group_B=Group_B.dropna().sort_values()
    
    #Volatility_monthly_factor select stocks in Group_B
    Group_B=(Volatility_monthly_factor.loc[group_B])[[str(m)]]
    Group_B=Group_B.dropna().sort_values([str(m)])
    
    Group_A_selected=Group_A.iloc[:int(Group_A.shape[0]*0.7)]
    Group_B_selected=Group_B.iloc[int(Group_B.shape[0]*0.7):]
    
    selected_stocks_monthly=Group_A_selected.index.tolist()+Group_B_selected.index.tolist()
    
    monthly_selected_stocks=pd.DataFrame({m:selected_stocks_monthly})
    Selected_stocks_monthly=pd.concat([Selected_stocks_monthly,monthly_selected_stocks],axis=1)
    
Selected_stocks_monthly.to_csv("/Users/lilychen/Desktop/dissertation/Results/Selected_stocks_monthly_ZZ500.csv",index=False)
