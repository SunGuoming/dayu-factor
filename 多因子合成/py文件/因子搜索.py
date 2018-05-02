from jaqs_fxdayu.util import dp
from jaqs.data.dataapi import DataApi
from jaqs_fxdayu.data import RemoteDataService

data_config = {
    "remote.data.address": "tcp://data.tushare.org:8910",
    "remote.data.username": "18222272839",
    "remote.data.password": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MjIxMzM5NzY0MzUiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTgyMjIyNzI4MzkifQ.cPLnbs3mFP9uIeZ7o1wDrxwaDAsMAGZJ9l-hJZVCv5k"
}
ds = api = RemoteDataService()
ds.init_from_config(data_config)


#注意在此设置日期和板块！！！
start = 20100101
end = 20161231
stock_symbol = list(set(dp.index_cons(ds, "000906.SH", start, end).symbol.values))

factor_list = ['volume', 'pb', 'roe','pe','share_trans_ratio']
check_factor = ','.join(factor_list)

import jaqs_fxdayu
jaqs_fxdayu.patch_all()
from jaqs_fxdayu.data import DataView
from jaqs.data import RemoteDataService
from jaqs_fxdayu.data.dataservice import LocalDataService
import os
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

dataview_folder = 'E:/data/data'
dv = DataView()
ds = LocalDataService(fp=dataview_folder)


factor_list = ['volume']
check_factor = ','.join(factor_list)

dv_props = {'start_date': start, 'end_date': end, 'symbol':','.join(stock_symbol),
         'fields': check_factor,
         'freq': 1,
         "prepare_fields": True}

dv.init_from_config(dv_props, data_api=ds)
dv.prepare_data()

# 读取所有dayu因子，保存在Factorlist中
df = pd.read_excel('Factors_Data.xlsx',sheetname=None)
df = pd.Panel(df)
FactorList = set({})
for i in range(df.loc[:,:,'name'].T.values.shape[0]):
    FactorList |= set(df.loc[:,:,'name'].T.values[i])
FactorList = list(FactorList)

i=0
for name in FactorList:
    dv.add_field(name)
    i=i+1
    print('导入进度%s'%(i/len(FactorList)))
    print('总体进度%s' % (i / (3*len(FactorList))))

alpha_signal = list(set(dv.fields)&set(FactorList))
dv.add_field('sw1')


sw1 = dv.get_ts('sw1')
dict_classify = {'480000': '银行', '430000': '房地产', '460000': '休闲服务', '640000': '机械设备', '240000': '有色金属', '510000': '综合', '410000': '公用事业', '450000': '商业贸易', '730000': '通信', '330000': '家用电器', '720000': '传媒', '630000': '电气设备', '270000': '电子', '490000': '非银金融', '370000': '医药生物', '710000': '计算机', '280000': '汽车', '340000': '食品饮料', '220000': '化工', '210000': '采掘', '230000': '钢铁', '650000': '国防军工', '110000': '农林牧渔', '420000': '交通运输', '620000': '建筑装饰', '350000': '纺织服装', '610000': '建筑材料', '360000': '轻工制造'}
sw1_name = sw1.replace(dict_classify)

id_zz500 = dp.daily_index_cons(api, "000300.SH", start, end)
id_hs300 = dp.daily_index_cons(api, "000905.SH", start, end)

columns_500 = list(set(id_zz500.columns)-set(id_hs300.columns))
import pandas as pd
id_member = pd.concat([id_zz500[columns_500],id_hs300],axis=1)
mask = ~id_member
import numpy as np

# 定义可买卖条件——未停牌、未涨跌停
def limit_up_down():
    trade_status = dv.get_ts('trade_status').fillna(0)
    mask_sus = trade_status == 0
    # 涨停
    up_limit = dv.add_formula('up_limit', '(close - Delay(close, 1)) / Delay(close, 1) > 0.095', is_quarterly=False)
    # 跌停
    down_limit = dv.add_formula('down_limit', '(close - Delay(close, 1)) / Delay(close, 1) < -0.095', is_quarterly=False)
    can_enter = np.logical_and(up_limit < 1, ~mask_sus) # 未涨停未停牌
    can_exit = np.logical_and(down_limit < 1, ~mask_sus) # 未跌停未停牌
    return can_enter,can_exit
can_enter,can_exit = limit_up_down()
import numpy as np

price = dv.get_ts('close_adj')
sw1 = sw1_name
enter = can_enter
exit =  can_exit
mask = mask
from jaqs_fxdayu.research.signaldigger.process import neutralize
neutralize_dict={}
i=0
for a in alpha_signal:
    neutralize_dict[a]=neutralize(factor_df = dv.get_ts(a), group = dv.get_ts("sw1")) #行业中性化处理
    i=i+1
    print('处理进度%s'%(i/len(alpha_signal)))
    print('总体进度%s'%(i/(3*len(alpha_signal))))
#     except:
#         print(str(a)+'异常')

import matplotlib.pyplot as plt
from jaqs_fxdayu.research import SignalDigger
from jaqs_fxdayu.research.signaldigger import analysis

def cal_obj(signal, name, period, quantile):
#     price_bench = dv.data_benchmark
    obj = SignalDigger(output_folder="FACTORS/%s" % name,
                       output_format='pdf')
    obj.process_signal_before_analysis(signal,
                                   price=price,
                                   n_quantiles=quantile, period=period,
                                   mask=mask,
                                   group=sw1,
                                   can_enter = enter,
                                   can_exit = exit,
                                   commission = 0.0008
                                   )
    return obj

def plot_pfm(signal, name, period=5, quantile=5):
    obj = cal_obj(signal, name, period, quantile)
    plt.show()
def signal_data(signal, name, period=5, quantile=5):
    obj = cal_obj(signal, name, period, quantile)
    return obj.signal_data

signals_dict = {a:signal_data(neutralize_dict[a], a, 20) for a in alpha_signal}
ic_pn = pd.Panel({a: analysis.ic_stats(signals_dict[a]) for a in signals_dict.keys()})
alpha_performance = round(ic_pn.minor_xs('return_ic'),2)

alpha_performance=alpha_performance.T
alpha_performance['IC_IR']=alpha_performance['IC Mean']*alpha_performance['Ann. IR']
#按IC与IR的乘积降序排列
alpha_performance=alpha_performance.sort_index(axis = 0,ascending = False,by = 'IC_IR')

alpha_performance.to_excel('因子搜索.xlsx')