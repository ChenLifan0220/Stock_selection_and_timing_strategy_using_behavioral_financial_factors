#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 10:58:19 2018

@author: lilychen
"""

import pandas as pd
import csv as csv
import numpy as np
import time
import matplotlib.pyplot as plt

close_price_original_100=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ100_all_close_price.csv",sep=",",index_col=0)
close_price_original_500=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ500_all_close_price.csv",sep=",",index_col=0)
monthly_volume_100=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_volume.csv",sep=",",index_col=0)
monthly_volume_500=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_volume.csv",sep=",",index_col=0)
turnover_original_100=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_turnover_ratio.csv",sep=",",index_col=0)
turnover_original_500=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_turnover_ratio.csv",sep=",",index_col=0)
deal_price_original_100=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_average_price.csv",sep=",",index_col=0)
deal_price_original_500=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_average_price.csv",sep=",",index_col=0)
capital_original_100=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/Original_factor_data/ZZ100_all_capital.csv",sep=",",index_col=0)
capital_original_500=pd.read_csv("/Users/lilychen/Desktop/dissertation/Data_Set/Factors/Original_factor_data/ZZ500_all_capital.csv",sep=",",index_col=0)

stock_code_list_100=monthly_volume_100.index.tolist()
stock_code_list_500=monthly_volume_500.index.tolist()

#select available stocks according to volume
for s in stock_code_list_100:
    single_stock=monthly_volume_100.loc[s]
    if single_stock.count()<110:
        monthly_volume_100=monthly_volume_100.drop(s)

#process nan value in volume
monthly_volume_100=monthly_volume_100.fillna(method='ffill',axis=1)
        
for s in stock_code_list_500:
    single_stock=monthly_volume_500.loc[s]
    if single_stock.count()<110:
        monthly_volume_500=monthly_volume_500.drop(s)

#process nan value in volume
monthly_volume_500=monthly_volume_500.fillna(method='ffill',axis=1)
        
stock_code_list_100=monthly_volume_100.index.tolist()
stock_code_list_500=monthly_volume_500.index.tolist()

#get monthly close price (100 and 500)
monthly_sequence=monthly_volume_100.columns.values.tolist()
daily_sequence=close_price_original_100.columns.values.tolist()

monthly_close_100=pd.DataFrame(index=close_price_original_100.index)
monthly_close_500=pd.DataFrame(index=close_price_original_500.index)

for no1 in monthly_sequence:
    for no2 in daily_sequence:
        if no2==no1:
            monthly_close_100=pd.concat([monthly_close_100,close_price_original_100[no1]],axis=1)
            monthly_close_500=pd.concat([monthly_close_500,close_price_original_500[no1]],axis=1)

monthly_close_100=monthly_close_100.loc[stock_code_list_100]
monthly_close_500=monthly_close_500.loc[stock_code_list_500]

#get monthly capital factor
capital_original_100=capital_original_100.loc[stock_code_list_100]
capital_original_500=capital_original_500.loc[stock_code_list_500]
capital_original_100=capital_original_100.fillna(method='ffill',axis=1)
capital_original_500=capital_original_500.fillna(method='ffill',axis=1)
capital_original_100=capital_original_100[monthly_sequence]
capital_original_500=capital_original_500[monthly_sequence]

#get monthly return
shift100_monthly=monthly_close_100.shift(-1,axis=1)
return_monthly_100=shift100_monthly/monthly_close_100-1
return_monthly_100=return_monthly_100.shift(1,axis=1)

shift500_monthly=monthly_close_500.shift(-1,axis=1)
return_monthly_500=shift500_monthly/monthly_close_500-1
return_monthly_500=return_monthly_500.shift(1,axis=1)

return_monthly_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_return.csv")
return_monthly_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_return.csv")

#get daily return
shift100_daily=close_price_original_100.shift(-1,axis=1)
return_daily_100=shift100_daily/close_price_original_100-1

shift500_daily=close_price_original_500.shift(-1,axis=1)
return_daily_500=shift500_daily/close_price_original_500-1

#get volatility
Std_100=pd.DataFrame(index=monthly_sequence)
for s in stock_code_list_100:
    single_stock=return_daily_100.loc[s]
    std_series=[]
    for no1 in range(len(monthly_sequence)):
        for no2 in range(len(daily_sequence)):
            if daily_sequence[no2]==monthly_sequence[no1]:
                if no2>20:
                    std=single_stock[(no2-20):no2]
                    std_series.append(std.std())
                else:
                    std_series.append(np.nan)
    
    single_std_series=pd.DataFrame({s:std_series},index=monthly_sequence)
    Std_100=pd.concat([Std_100,single_std_series],axis=1)
Std_100=Std_100.T
    
Std_500=pd.DataFrame(index=monthly_sequence)
for s in stock_code_list_500:
    single_stock=return_daily_500.loc[s]
    std_series=[]
    for no1 in range(len(monthly_sequence)):
        for no2 in range(len(daily_sequence)):
            if daily_sequence[no2]==monthly_sequence[no1]:
                if no2>20:
                    std=single_stock[(no2-20):no2]
                    std_series.append(std.std())
                else:
                    std_series.append(np.nan)
    
    single_std_series=pd.DataFrame({s:std_series},index=monthly_sequence)
    Std_500=pd.concat([Std_500,single_std_series],axis=1)
Std_500=Std_500.T

daily_close_100=close_price_original_100.loc[stock_code_list_100]
daily_close_500=close_price_original_500.loc[stock_code_list_500]
turnover_original_100=turnover_original_100.loc[stock_code_list_100]
turnover_original_500=turnover_original_500.loc[stock_code_list_500]
deal_price_original_100=deal_price_original_100.loc[stock_code_list_100]
deal_price_original_500=deal_price_original_500.loc[stock_code_list_500]
    
Std_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/factors/ZZ100_all_volatility.csv")
Std_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/factors/ZZ500_all_volatility.csv")
capital_original_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/factors/ZZ100_all_capital.csv")
capital_original_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/factors/ZZ500_all_capital.csv")
monthly_volume_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_volume.csv")
monthly_volume_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_volume.csv")
daily_close_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ100_all_close_price.csv")
daily_close_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/DataZZ500_all_close_price.csv")
turnover_original_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_turnover_ratio.csv")
turnover_original_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_turnover_ratio.csv")
deal_price_original_100.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ100_all_average_price.csv")
deal_price_original_500.to_csv("/Users/lilychen/Desktop/dissertation/Data_Set/ZZ500_all_average_price.csv")