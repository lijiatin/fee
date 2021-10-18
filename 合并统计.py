import pandas as pd
#大商所文件需要删除首行


pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width',1000)

fpath_shfe = r'H:\File\交易所手续费\shfe.csv'
fpath_dce =  r'H:\File\交易所手续费\dce.xls'
fpath_zce =  r'H:\File\交易所手续费\zce.xls'


def fuc_shfe(fpath=r'H:\File\上期所210913.csv'):
    df = pd.read_csv(fpath)

    def fuc(x):
        if x[r'交易手续费额(元/手)'] != 0:
            return 0.01 * ((x[r'投机买保证金率(%)'] + x[r'投机卖保证金率(%)'])/2) * (x[r'交易手续费额(元/手)']+x[r'交易手续费额(元/手)']*x[r'平今折扣率(%)']/100)/x[r'结算价']*10000
        else:
            return 0.001*(x[r'交易手续费率(‰)'] + x[r'交易手续费率(‰)'] * x[r'平今折扣率(%)']/100)/2 * ((x[r'投机买保证金率(%)'] + x[r'投机卖保证金率(%)'])/2*0.01)*10000
    df['per_fee'] = df.apply(fuc, axis=1)
    df = df.sort_values(by='per_fee')
    dfx = pd.DataFrame()
    dfx['instru'] = df[u'合约代码']
    dfx['当日结算价'] = df[u'结算价'].astype('float')
    dfx['exchange'] = 'SHFE'
    dfx['marginrate'] = (df[u'投机买保证金率(%)'] + df[u'投机卖保证金率(%)'])/2
    dfx['per_fee'] = df['per_fee']
    return dfx


def fuc_dce(fpath=r'H:\File\1631470712021.xls'):
    df = pd.read_excel(fpath)

    def fuc(x):
        if x[u'手续费收取方式'] == u'绝对值':
            return 0.01*int(x[u'投机买保证金率'][:-1])*(x[u'短线开仓手续费']+x[u'短线平仓手续费'])/(2 * float(x[u'结算价'].replace(r',', '')))*10000
        else:
            return 0.0001*(x[u'短线开仓手续费']+x[u'短线平仓手续费'])/2*int(x[u'投机买保证金率'][:-1])*0.01*10000
    df['per_fee'] = df.apply(fuc, axis=1)
    df = df.sort_values(by='per_fee')
    dfx = pd.DataFrame()
    dfx['instru'] = df[u'合约代码']
    dfx['当日结算价'] = df[u'结算价'].map(lambda x: float(x.replace(r',', '')))
    dfx['exchange'] = 'DCE'
    dfx['marginrate'] = df[u'投机买保证金率'].map(lambda x: int(x[:-1]))
    dfx['per_fee'] = df['per_fee']
    return dfx


def fuc_zce(fpath=r'H:\File\郑商所210930.xls'):
    df = pd.read_excel(fpath)

    def fuc(x):
        if x[u'是否单边市'] == u'N':
            return 0.01*(x[u'交易保证金率(%)'])*(x[u'交易手续费']+x[u'日内平今仓交易手续费'])/(2 * float(x[u'当日结算价'].replace(r',', '')))*10000
        else:
            return 100000
    df['per_fee'] = df.apply(fuc, axis=1)
    df = df.sort_values(by='per_fee')
    dfx = pd.DataFrame()
    dfx['instru'] = df[u'合约代码']
    dfx['当日结算价'] = df[u'当日结算价'].map(lambda x: float(x.replace(r',', '')))
    dfx['exchange'] = 'ZCE'
    dfx['marginrate'] = df[u'交易保证金率(%)']
    dfx['per_fee'] = df['per_fee']
    return dfx


list_fpath = [fpath_shfe, fpath_dce, fpath_zce]
list_fuc = [fuc_shfe, fuc_dce, fuc_zce]

result = []
for i in range(3):
    result.append(list_fuc[i](list_fpath[i]))

df_r = pd.concat(result,ignore_index=True)
df_r['每点盈亏率与费率比'] = ((1/(0.01*df_r['marginrate']))/df_r['当日结算价'])/df_r['per_fee']
df_r =df_r.sort_values(by='每点盈亏率与费率比',ascending=False).reset_index()
print(df_r.head(1000))
