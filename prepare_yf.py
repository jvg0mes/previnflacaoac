
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as st
from datetime import datetime as dt


# IMPORTANDO ARQUIVOS DE METADADOS
yf_md = pd.read_csv('data/yf_metadata.csv',encoding='latin-1',sep=';')


# IMPORTANDO ARQUIVOS DE SERIES
yf_s = pd.read_csv('data/yf_series.csv',encoding='latin-1',sep=';',index_col='Date')


cframe = yf_s.copy()


cframe = cframe[pd.to_datetime(cframe.index) < pd.to_datetime('08/01/2022')]


cframe = cframe[pd.to_datetime(cframe.index) >= pd.to_datetime('01/01/2013')]


sum(cframe.isna().sum(axis=0)<3)


cframe = cframe[(cframe.isna().sum(axis=0)<3).replace({False:np.NaN}).dropna().index]


cframe = cframe.shift(1).dropna()


len(cframe.columns)

cframe


nonvar_columns = cframe.columns

cframe.isna().sum().sum()


cframe.loc[:,np.isin(cframe.columns,nonvar_columns.astype(str))]= \
    (cframe.loc[:,np.isin(cframe.columns,nonvar_columns.astype(str))].diff(1)/ \
    cframe.loc[:,np.isin(cframe.columns,nonvar_columns.astype(str))].shift(1))*100


cframe = cframe.iloc[1:,:]


cframe


cframe = cframe[(cframe.isna().sum(axis=0)<=0).replace({False:np.NaN}).dropna().index]


cframe


cframe = cframe.replace({np.inf:0,-np.inf:0})


tmp = cframe*cframe


tmp.columns = [c + '_e2' for c in tmp.columns]


cframe = pd.concat([cframe,tmp],axis=1)


from ta.trend import sma_indicator


for slen in [3,6,12]:
    tmp = cframe.apply(lambda x: sma_indicator(x,slen),axis=0)
    tmp.columns = [c + '_sma' + str(slen) for c in tmp.columns]
    cframe = pd.concat([cframe,tmp],axis=1)



cframe = cframe.dropna()


adframe = cframe.apply(lambda x: st.adfuller(x)[1],axis=0)


stat0 = (round(adframe,3)<=0.050).replace({False:np.NaN}).dropna().index


nonstat0 = (round(adframe,3)>0.050).replace({False:np.NaN}).dropna().index


tmp = cframe.loc[:,nonstat0].diff(1)/cframe.loc[:,nonstat0].shift(1)


tmp = tmp.replace({np.inf:0,-np.inf:0})


adframe1 = tmp.apply(lambda x: st.adfuller(x.dropna())[1],axis=0)


stat1 = (round(adframe1,3)<=0.050).replace({False:np.NaN}).dropna().index


nonstat1 = (round(adframe1,3)>0.050).replace({False:np.NaN}).dropna().index


stat1


tmp = tmp[stat1]


tmp.columns = [v + '_o1' for v in tmp.columns]


final_frame = pd.concat([cframe[stat0],tmp],axis=1)


final_columns = list(stat0.copy())


final_columns.extend(list(tmp.columns))


final_frame


{'frame':final_frame,'features':stat0}


(final_frame.isna().sum(axis=0)<2).sum()


final_columns = (final_frame.isna().sum(axis=0)<2).replace({False:np.NaN}).dropna().index


final_columns


final_frame[final_columns].isna().sum()


final_frame[final_columns].dropna()


fdict = {'frame':final_frame[final_columns].dropna(),'features':final_columns}


fdict


fdict['frame'].to_csv('final_data/yfframe.csv',sep=';')


