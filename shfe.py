import pandas as pd
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 30)

df =  pd.read_csv(r'H:\File\上期所210913.csv')
def fuc(x):
    if x[r'交易手续费额(元/手)']!=0:
        return 0.01* ((x[r'投机买保证金率(%)'] + x[r'投机卖保证金率(%)'])/2) * (x[r'交易手续费额(元/手)']+x[r'交易手续费额(元/手)']*x[r'平今折扣率(%)']/100)/x[r'结算价']*10000
    else:
        return 0.001*(x[r'交易手续费率(‰)'] + x[r'交易手续费率(‰)']* x[r'平今折扣率(%)']/100)/2 * ((x[r'投机买保证金率(%)'] + x[r'投机卖保证金率(%)'])/2*0.01)*10000
df['per_fee'] = df.apply(fuc,axis=1)
df =df.sort_values(by='per_fee')
print(df)