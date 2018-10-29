#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:57:07 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt

Selected_stocks_monthly=pd.read_csv("/Users/lilychen/Desktop/dissertation/Results/Selected_stocks_monthly_ZZ500.csv",sep=",")
return_original=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv",sep=",",index_col=0)
Benchmark=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/HS300.csv",sep=",",index_col=0)

monthly_sequence=Selected_stocks_monthly.columns.values.tolist()
#New_monthly_sequence=[str(x) for x in monthly_sequence]
Benchmark=Benchmark.iloc[2:]

#Get Benchmark
for i in range(len(monthly_sequence)):
    Benchmark.iloc[i+1]=Benchmark.iloc[i+1]/Benchmark.iloc[0]
Benchmark=Benchmark.drop(Benchmark.index[0])

#Annualized_return
Monthly_return=[]
for m in monthly_sequence:
    monthly_return=(return_original.loc[(Selected_stocks_monthly[str(m)].dropna()).values.tolist(),str(m)].mean())*0.984
    Monthly_return.append(monthly_return)
Monthly_return=pd.DataFrame({'monthly_return':Monthly_return},index=monthly_sequence)

net_value=(np.array(Monthly_return)+1).cumprod()

#Compound_Annualized_return
def Compound_Annualized_return(a):
    Compound_Annualized_return=1
    for m in range(len(a)):
        Compound_Annualized_return=Compound_Annualized_return*(1+a[m])
    return float(pow(Compound_Annualized_return,12/len(a))-1)

#Simple_Annualized_return
def Simple_Annualized_return(a):
    return a.sum()/len(a)*12

#Netvalue_Curve
def Netvalue_Curve(a):
    return (np.array(a)+1).cumprod()

#Sharpe_Ratio
def Sharp_ratio(a):
    return np.sqrt(12) * a.mean()/a.std()

#Max_Drawdown
def Max_drawdown_ratio(arr):
    # the end point. (Build the series of the highest point in history, find the smallest ratio point )
    i=np.argmax((np.maximum.accumulate(arr)-arr)/np.maximum.accumulate(arr))
    # the start point. （Find the highest point befort the end point)
    j=np.argmax(arr[:i])
    return (arr[j]-arr[i])/arr[j]

def Max_drawdown(arr):
    # the end point. (Build the series of the highest point in history, find the smallest ratio point )
    i=np.argmax((np.maximum.accumulate(arr)-arr))
    # the start point. （Find the highest point befort the end point)
    j=np.argmax(arr[:i])
    return arr[j]-arr[i]

#Performance
def Performance(return_list, index_num):
    index_value=index_num.shift(1,axis=0)/index_num-1
    index_value.iloc[0]=index_num.iloc[0]-1
    return_strategy=return_list.values
    return_benchmark=index_num.values
    index_value=index_value.values
    
    return_difference=return_strategy-return_benchmark
    st1=(return_strategy.std())*(12**0.5)
    st2=(return_benchmark.std())*(12**0.5)

    print("-----------------------------------------------------")
    print("Volatility of strategy is " + str(round(st1,4)))
    print("Volatility of benchmark is " + str(round(st2,4)))

    sp1=Sharp_ratio(return_strategy)
    sp3=Sharp_ratio(return_benchmark)
    ir=Sharp_ratio(return_difference)

    print("-----------------------------------------------------")
    print("Sharp ratio of strategy is " + str(round(sp1,4)))
    print("Sharp ratio of benchmark is " + str(round(sp3,4)))
    print("-----------------------------------------------------")
    print("Information ratio of strategy is " + str(round(ir,4)))
    
    net_worth_original=Netvalue_Curve(return_list)
    
    n=list(net_worth_original)
    n.insert(0,1)
    net_worth=np.array(n)
    
    mdr1=float(Max_drawdown_ratio(net_worth))
    mdr3=float(Max_drawdown_ratio(index_value))
    
    print("-----------------------------------------------------")
    print("Max drawdown ratio of strategy is " + str(round(mdr1,4)))
    print("Max drawdown ratio of benchmark is " + str(round(mdr3,4)))
    
    md1=float(Max_drawdown(net_worth))
    md3=float(Max_drawdown(index_value))
    print("-----------------------------------------------------")
    print("Max drawdown of strategy is " + str(round(md1,4)))
    print("Max drawdown of benchmark is " + str(round(md3,4)))
    
    compound_anualized_return=Compound_Annualized_return(return_strategy)
    simple_anualized_return=Simple_Annualized_return(return_strategy)
    print("-----------------------------------------------------")
    print("Compound annualized rate of return is " + str(round(compound_anualized_return,4)))
    print("Simple annualized rate of return is " + str(round(simple_anualized_return,4)))
    
    
Performance(Monthly_return,Benchmark)



