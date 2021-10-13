import pandas as pd
pd.set_option('display.max_rows', 300)
df =  pd.read_excel(r'H:\File\1631470712021.xls')
#计算方式 开仓保证金率*单笔手续费/结算价
def fuc(x):
    if x[u'手续费收取方式']==u'绝对值':
        return 0.01*int(x[u'投机买保证金率'][:-1])*(x[u'短线开仓手续费']+x[u'短线平仓手续费'])/(2 * float( x[u'结算价'].replace(r',','')))*10000
    else:
        return 0.0001*(x[u'短线开仓手续费']+x[u'短线平仓手续费'])/2*int(x[u'投机买保证金率'][:-1])*0.01*10000
df['per_fee'] = df.apply(fuc,axis=1)
df =df.sort_values(by='per_fee')
print(df)