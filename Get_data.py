from WindPy import *
w.start()
import pandas as pd
import numpy as np
import copy
import datetime
import math
import re
# import date

w_tdays = w.tdays("2007-01-13", "2018-06-29", "")
time_list = pd.DataFrame(w_tdays.Data).T

trading_day = []
for t in time_list[0]:
    day = re.sub(r'\D', "", re.sub(r' .*$', "", str(t)))
    trading_day.append(day)

volumn_list100 = []
volumn_list500 = []

for Time in trading_day:
    Time = str(Time)
    time = datetime.datetime.strptime(Time, '%Y%m%d').strftime('%Y-%m-%d')
    trade_date = time[:4] + time[5:7] + time[-2:]
    #中证100成分股
    ZZ100 = w.wset("sectorconstituent","date="+time+";sectorid=a001030204000000;field=wind_code").Data[0]
    #中证500成分股
    ZZ500 = w.wset("sectorconstituent","date="+time+";sectorid=1000008491000000;field=wind_code").Data[0]

    #close
    Data_100 = w.wss(ZZ100, "free_turn","tradeDate=" + trade_date + ";priceAdj=F;cycle=D")
    Data_500 = w.wss(ZZ500, "free_turn","tradeDate=" + trade_date + ";priceAdj=F;cycle=D")

    DataFrame_100 = pd.DataFrame(Data_100.Data, index=Data_100.Fields,columns=Data_100.Codes).T
    DataFrame_100.columns = [Time]
    DataFrame_500 = pd.DataFrame(Data_500.Data, index=Data_500.Fields,columns=Data_500.Codes).T
    DataFrame_500.columns = [Time]
    
    volumn_list100.append(DataFrame_100)
    volumn_list500.append(DataFrame_500)

#    #Excel 输出
#    DataFrame_100.to_csv('D:\\General\\0_Lily\\Data\\'+trade_date + '_ZZ100_volume' + '.csv', encoding='utf_8')

    print('TIME = ', time)
 
a = pd.concat(volumn_list100, axis = 1)
b = pd.concat(volumn_list500, axis = 1)

a.to_csv('D:\\General\\0_Lily\\'+'ZZ100_turnover_ratio' + '.csv', encoding='utf_8')
b.to_csv('D:\\General\\0_Lily\\'+'ZZ500_turnover_ratio' + '.csv', encoding='utf_8')

