import pandas as pd
pd.set_option('display.max_rows', 300)
df =  pd.read_excel(r'H:\File\郑商所210930.xls')
def fuc(x):
    if x[u'是否单边市']==u'N':
        return 0.01*(x[u'交易保证金率(%)'])*(x[u'交易手续费']+x[u'日内平今仓交易手续费'])/(2 * float( x[u'当日结算价'].replace(r',','')))*10000
    else:
        return 100000
df['per_fee'] = df.apply(fuc,axis=1)
df =df.sort_values(by='per_fee')
print(df)  