import ipeadatapy as ipea
import pandas as pd
import numpy as np

tm = ipea.themes()

md = ipea.metadata()

md.columns

#Observando series de preços
md[md['CODE'].str.contains('IPCA')]

#Separando serie escolhida
y_code = 'PRECOS12_IPCA12'

#filtrando somente series ativas
md = md[md['SERIES STATUS'] == 'A'].reset_index().iloc[:,1:]

#selecionando temas da tabela tm
temas = tm['ID'].unique()

#filtrando series com frequencia mensal
md = md[md.FREQUENCY == 'Mensal'].reset_index().iloc[:,1:]

#formatando data do campo ultima atualizacao
md['LAST UPDATE'] = pd.to_datetime(md['LAST UPDATE'])

#filtrando series que apresentam defasagem de atualizacao
md = md[md['LAST UPDATE']. \
apply(lambda x: x.year + x.month/100) == 2022.07]. \
reset_index().iloc[:,1:]

#criando tabela para separar temas por nome
rel_temas = tm[np.isin(tm['ID'],temas)]. \
    reset_index().iloc[:,1:]

#depara tema nome
dtm = dict(zip(rel_temas['ID'],rel_temas['NAME']))

#criando coluna de nome do tema
md['THEME'] = md['THEME CODE'].replace(dtm)

#controle para saber a disposicao desejada da tabela
disp = 'v' #h or v (v: util para analise no power bi ou em outro software relacional)

#importando decorador timeout para interromper execucao apos um tempo
from timeout import timeout

@timeout(10) # Garante que uma serie nao carregue eternamente
def get_serie(lobj,disp='v'):

    # separa a linha a ser trabalhada
    #lobj = md.iloc[l,:]
    # obtem o dataframe do codigo daquela linha
    obj = ipea.timeseries(lobj['CODE'])
    # renomeia a coluna de valor para o codigo da serie
    if disp == 'h':
        obj.rename({obj.columns[len(obj.columns)-1]:obj['CODE'].unique()[0]},
                axis=1,inplace=True)
        obj.drop(['RAW DATE','CODE'],axis=1,inplace=True)
    else:
        obj.rename({obj.columns[len(obj.columns)-1]:"VALUE"},
            axis=1,inplace=True)
        obj.drop(['RAW DATE'],axis=1,inplace=True) # Faltou o inplace
    
    return(obj)

# loop para percorrer todas as series
for x in range(0,len(md)):
    # importa a serie e e cria o df se for a primeira execucao
    if x == 0:
        print('Iniciando serie ' + md.loc[x,'CODE'])
        try:
            df = get_serie(md.loc[x,:],disp='h') #
        except:
            next()
        print('Serie ' + md.loc[x,'CODE'] + " importada!")
    else:
        # importa a serie e concatena ao dataframe
        try:
            print('Iniciando serie ' + md.loc[x,'CODE'])
            df = pd.concat([df,get_serie(md.loc[x,:],disp='h')],axis=1)
            print('Serie ' + md.loc[x,'CODE'] + " importada!")
        except:
            print('Serie ' + md.loc[x,'CODE'] + ' falhou!')

# excluindo timezone pois o excel nao permite
md['LAST UPDATE'] = md['LAST UPDATE'].apply(lambda x: x.replace(tzinfo = None))

# obtendo tabela com valores da variavel independente
obj = ipea.timeseries(y_code)
obj.rename({obj.columns[len(obj.columns)-1]:"VALUE"},
    axis=1,inplace=True)

df = df[df.iloc[:,0] >= 2000]
df = df.drop(['YEAR','DAY','MONTH'],axis=1)

obj = obj[obj['YEAR'] >= 2000]
obj['VAR_3'] = (obj['VALUE'].diff(3)/obj['VALUE'].shift(3))*100
obj = obj.drop('VALUE',axis=1)

obj.drop(['YEAR','MONTH','DAY','CODE','RAW DATE'],axis=1,inplace=True)

df.to_csv('data/ipeadata_series.csv',sep=';')
obj.to_csv('data/target.csv',sep=';')
md.to_csv('data/ipeadata_metadata.csv',sep=';',index=None)

c = pd.concat([obj,df],axis=1).corr()[['VAR_3']]
best_c = (c['VAR_3'].abs().sort_values().drop('VAR_3')>.4).replace({False:np.NaN}).dropna()

df[best_c.index]



























