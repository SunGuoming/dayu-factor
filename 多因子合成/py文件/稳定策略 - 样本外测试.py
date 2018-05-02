from jaqs_fxdayu.data import DataView
from jaqs_fxdayu.data import RemoteDataService
import os
import numpy as np
import warnings
from jaqs_fxdayu.util import dp
warnings.filterwarnings("ignore")

data_config = {
    "remote.data.address": "tcp://data.tushare.org:8910",
    "remote.data.username": "18222272839",
    "remote.data.password": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MjIxMzM5NzY0MzUiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTgyMjIyNzI4MzkifQ.cPLnbs3mFP9uIeZ7o1wDrxwaDAsMAGZJ9l-hJZVCv5k"
}

ds = RemoteDataService()
ds.init_from_config(data_config)
DV = DataView()

start=20170101
end=20180501
stock_symbol = list(set(dp.index_cons(ds, "000906.SH", start, end).symbol.values))
zz800_props = {'start_date': start, 'end_date': end,  'symbol':','.join(stock_symbol),
               'fields': 'pb,pe,ps,float_mv,sw1,volume',
               'freq': 1,
               "prepare_fields": True}

def save_zz800(props):
    dataview_folder = 'JAQS_Data/Mutifactor_1'
    if not (os.path.isdir(dataview_folder)):
        os.makedirs(dataview_folder)
    DV.init_from_config(props, ds)
    DV.prepare_data()
    DV.save_dataview(dataview_folder)
    return


save_zz800(zz800_props)

dataview_folder = 'JAQS_Data/Mutifactor_1'
dv = DataView()
dv.init_from_config(zz800_props, ds)
dv.load_dataview(dataview_folder)

import talib as ta
import numpy as np
import pandas as pd
from datetime import datetime

def change_time(df):
    df.index = pd.Index(map(lambda x: datetime.strptime(str(x),"%Y%m%d") , df.index))
    return df

EMA=dv.get_ts('close').ewm(span=5, adjust=False).mean()
EMA2=EMA.ewm(span=5, adjust=False).mean()
EMA3=EMA2.ewm(span=5, adjust=False).mean()
dv.append_df(EMA3,'EMA3')
dv.add_formula('a','close/Delay(close,1)-1',is_quarterly=False, add_data=True)
dv.add_formula('b','(close/Delay(EMA3,19))^(1/20)-1',is_quarterly=False, add_data=True)
Factor1 = dv.add_formula('Factor1',
                          '-Log((Ts_Sum(If(a>b,1,0),20)-1)*Ts_Sum(If(a<b,(a-b)^2,0),20)/(Ts_Sum(If(a<b,1,0),20))*Ts_Sum(If(a>b,(a-b)^2,0),20))',
                          is_quarterly=False, add_data=True)


EMA=dv.get_ts('close').ewm(span=60, adjust=False).mean()
dv.append_df(EMA,'EMA')
Factor2 = dv.add_formula('Factor2',
                          '-ps',
                          is_quarterly=False, add_data=True)

Factor3 = dv.add_formula('Factor3',
                          '-pb',
                          is_quarterly=False, add_data=True)

r = dv.add_formula('dayr_20','close/Delay(close,10)',is_quarterly=False, add_data=True)
Factor4 = dv.add_formula('Factor4','-pe',is_quarterly=False, add_data=True)


dv.add_formula('VOL240','Ts_Sum(volume/capital_stk,%s)/%s'%(240,240),is_quarterly=False, add_data=True)
dv.add_formula('VOL10','Ts_Sum(volume/capital_stk,%s)/%s'%(10,10),is_quarterly=False, add_data=True)
dv.add_formula('VOL5','Ts_Sum(volume/capital_stk,%s)/%s'%(5,5),is_quarterly=False, add_data=True)


Factor5 = dv.add_formula('Factor5','-VOL240-3*VOL10',is_quarterly=False, add_data=True)

Factor6 = dv.add_formula('Factor6','-VOL10*(dayr_20)-VOL10',is_quarterly=False, add_data=True)

EMA13=dv.get_ts('close').ewm(span=13, adjust=False).mean()
dv.append_df(EMA13,'EMA13')
dv.add_formula('BullPower','high-EMA13',is_quarterly=False, add_data=True)
Factor7 = dv.add_formula('Factor7','-Abs(VOL5-0.005)',is_quarterly=False, add_data=True)

dv.add_formula('a','close/Delay(close,1)-1',is_quarterly=False, add_data=True)
Factor8 = dv.add_formula('Factor8','-Ts_Sum(Max(a,0),20)',is_quarterly=False, add_data=True)

Factor9 = dv.add_formula('Factor9','-ps-pb-0.1*pe',is_quarterly=False, add_data=True)
Factor10 = dv.add_formula('Factor10','-BullPower*volume',is_quarterly=False, add_data=True)

alpha_signal = ['Factor1','Factor7','Factor9']
for a in alpha_signal:
    print((dv.get_ts(a)).shape)

import matplotlib.pyplot as plt
from jaqs_fxdayu.research import SignalDigger
from jaqs_fxdayu.util import dp

def limit_up_down():
    # 定义可买卖条件——未停牌、未涨跌停
    trade_status = dv.get_ts('trade_status')
    mask_sus = trade_status != 1
    # 涨停
    dv.remove_field('up_limit')
    dv.add_formula('up_limit', '(close - Delay(close, 1)) / Delay(close, 1) > 0.095', is_quarterly=False, add_data=True)
    # 跌停
    dv.remove_field('down_limit')
    dv.add_formula('down_limit', '(close - Delay(close, 1)) / Delay(close, 1) < -0.095', is_quarterly=False, add_data=True)
    can_enter = np.logical_and(dv.get_ts('up_limit') < 1, ~mask_sus) # 未涨停未停牌
    can_exit = np.logical_and(dv.get_ts('down_limit') < 1, ~mask_sus) # 未跌停未停牌
    return can_enter,can_exit

def cal_obj(signal, name, period=5, quantile=5):
    obj = SignalDigger()
    obj.process_signal_before_analysis(signal,
                                       price=price,
                                       n_quantiles=quantile,
                                       period=period,
                                       can_enter = can_enter,
                                       can_exit = can_exit,
                                       mask=mask,
                                       )
    obj.create_full_report()
    return obj


id_member = dp.daily_index_cons(ds, "000906.SH", start, end)
mask = id_member==0


can_enter,can_exit = limit_up_down()

from jaqs_fxdayu.research.signaldigger import multi_factor

period_list=[20]
factor_list=['Factor1','Factor7','Factor9']
ic = dict()
factors_dict = {signal:dv.get_ts(signal) for signal in factor_list}
for period in period_list:
    ic[period]=multi_factor.get_factors_ic_df(factors_dict,
                                              price=dv.get_ts("close_adj"),
                                              high=dv.get_ts("high_adj"), # 可为空
                                              low=dv.get_ts("low_adj"),# 可为空
                                              n_quantiles=5,# quantile分类数
                                              mask=mask,# 过滤条件
                                              can_enter=can_enter,# 是否能进场
                                              can_exit=can_exit,# 是否能出场
                                              period=period,# 持有期
                                              benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                              commission = 0.0008,
                                              )

ic_mean_table = pd.DataFrame(data=np.nan,columns=period_list,index=factor_list)
ic_std_table = pd.DataFrame(data=np.nan,columns=period_list,index=factor_list)
ir_table = pd.DataFrame(data=np.nan,columns=period_list,index=factor_list)
for signal in factor_list:
    for period in period_list:
        ic_mean_table.loc[signal,period]=ic[period][signal].mean()
        ic_std_table.loc[signal,period]=ic[period][signal].std()
        ir_table.loc[signal,period]=ic[period][signal].mean()/ic[period][signal].std()

factor_list = ['Factor1', 'Factor7', 'Factor9']
period = 20

from jaqs_fxdayu.research.signaldigger import process

factor_dict = dict()
index_member = id_member
for name in factor_list:
    signal = dv.get_ts(name)  # 调整符号
    print(name)

    signal = process.winsorize(factor_df=signal, alpha=0.05, index_member=index_member)  # 去极值
    #     print(signal.shape)
    signal = process.standardize(signal, index_member)  # z-score标准化 保留排序信息和分布信息
    #     print(signal.shape)
    #     signal = process.neutralize(signal,group=dv.get_ts("sw1"),float_mv = dv.get_ts("float_mv")) #行业中性化
    print(signal.shape)

    factor_dict[name] = signal

for name in factor_list:
    dv.append_df(factor_dict[name],name+'_J')

# rollback_period代表滚动窗口所用到的天数,即用前多少期的数据来计算现阶段的因子权重。 通常建议设置时间在半年以上,可以获得相对稳定的预期结果

period = 20 # 20天的持有期

#  多因子组合-动态加权参数配置
props = {
    'price':dv.get_ts("close_adj"),
    'high':dv.get_ts("high_adj"), # 可为空
    'low':dv.get_ts("low_adj"),# 可为空
    'ret_type': 'return',#可选参数还有upside_ret/downside_ret 则组合因子将以优化潜在上行、下行空间为目标
    'benchmark_price': dv.data_benchmark,  # 为空计算的是绝对收益　不为空计算相对收益
    'period': period, # 20天的持有期
    'mask': mask,
    'can_enter': can_enter,
    'can_exit': can_exit,
    'forward': True,
    'commission': 0.0008,
    "covariance_type": "shrink",  # 协方差矩阵估算方法 还可以为"simple"
    "rollback_period": 250}  # 滚动窗口天数

comb_factors = dict()
for method in ["equal_weight","ic_weight","ir_weight","max_IR","max_IC"]:
    signal = multi_factor.combine_factors(factor_dict,
                                                        standardize_type="rank",
                                                        winsorization=False,
                                                        weighted_method=method,
                                                        props=props)
    #z-score标准化
    comb_factors[method] = process.standardize(signal,index_member)

ic_20 = multi_factor.get_factors_ic_df(comb_factors,
                                         price=dv.get_ts("close_adj"),
                                         high=dv.get_ts("high_adj"), # 可为空
                                         low=dv.get_ts("low_adj"),# 可为空
                                         n_quantiles=5,# quantile分类数
                                         mask=mask,# 过滤条件
                                         can_enter=can_enter,# 是否能进场
                                         can_exit=can_exit,# 是否能出场
                                         period=period,# 持有期
                                         benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                         commission = 0.0008,
                                         )

ic_20_mean = dict()
ic_20_std = dict()
ir_20 = dict()
for name in ic_20.columns:
    ic_20_mean[name] = ic_20[name].loc[start:].mean()
    ic_20_std[name] = ic_20[name].loc[start:].std()
    ir_20[name] = ic_20_mean[name] / ic_20_std[name]

import datetime

trade_date = pd.Series(ic_20.index)
trade_date = trade_date.apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
ic_20.index = trade_date

obj = SignalDigger(output_folder='./output',
                   output_format='pdf')
obj.process_signal_before_analysis(signal=comb_factors["equal_weight"],
                                   price=dv.get_ts("close_adj"),
                                   high=dv.get_ts("high_adj"), # 可为空
                                   low=dv.get_ts("low_adj"),# 可为空
                                   n_quantiles=5,# quantile分类数
                                   mask=mask,# 过滤条件
                                   can_enter=can_enter,# 是否能进场
                                   can_exit=can_exit,# 是否能出场
                                   period=period,# 持有期
                                   benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                   commission = 0.0008,
                                   )
obj.create_full_report()
plt.show()