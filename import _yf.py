import pandas as pd
import numpy as np
from datetime import datetime as dt

#testando preço das commodities
import yfinance

clmd = pd.read_csv('data\yf_metadata.csv',sep=';')
cl = clmd['Symbol']


for x in cl:
    
    c = yfinance.Ticker(x).history(period='max',interval='1d')[['Close']]
    c['year'] = np.array(c.index.year)
    c['month'] = np.array(c.index.month)
    c['ym'] = c['year'].astype(str) + '-' + c['month'].astype(str)
    c['date'] = np.array(c.index)

    c = c.loc[c.groupby('ym')['date'].max().to_numpy(),['Close','year','month']].sort_index()
    c.index = pd.to_datetime(c['year'].astype(str) + '-' + c['month'].astype(str) + '-01')
    c = c.drop(['year','month'],axis=1)
    
    c.rename({'Close':x},axis=1,inplace=True)
    
    if x == cl[0]:
        cdf = c
    else:
        cdf = pd.concat([cdf,c],axis=1)

cdf.to_csv('data/yf_series.csv',sep =';')















