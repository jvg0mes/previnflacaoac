import pandas as pd
import numpy as np
from bcb import sgs

#lendo frame de metadados
bsl = pd.read_csv('data/bcb_metadata.csv',sep=';',encoding='latin-1')

#limpando colunas inutilizaveis
bsl = bsl[list((bsl.isna().sum(axis=0)>100). \
    replace({True:np.NaN}).dropna().index)]


#formatando data
bsl['Ultimo'] = pd.to_datetime(bsl['Ultimo'],format='%d/%m/%Y')

#selecionando somente series atualizadas
bsl = bsl[bsl['Ultimo']>=pd.to_datetime('04/01/2022')]

bsl = bsl.reset_index().iloc[:,1:]

#importando funcao do teste de raiz unitaria para detectar estacionariedade
from statsmodels.tsa.stattools import adfuller

#loop que importa as series e trabalha elas
#importando a serie

for x in bsl['Codigo']:

    try:
        obj = sgs.get((x,x))

        obj = obj[obj.index.year >2009]
        
        if x == bsl['Codigo'].iloc[0]:
            bdf = obj
        else:
            bdf = pd.concat([bdf,obj],axis=1)
            
        print(str(x) + ' sucesso!')

    except:
        print(str(x) + ' falha importacao!')

bdf.to_csv('data/bcb_series.csv',sep=';')
