import pandas as pd
factor=pd.read_excel('因子搜索.xlsx')
FactorList=list(factor.index[:10])

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

start = 20160101
end = 20180327
stock_symbol = list(set(dp.index_cons(ds, "000906.SH", start, end).symbol.values))

factor_list = ['volume', 'pb', 'roe','pe','share_trans_ratio','sw1']
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

for name in FactorList:
    dv.add_field(name)

import numpy as np

def mask_index_member():
    id_member = dp.daily_index_cons(api, "000906.SH", start, end)
    mask = id_member==0
    return mask

def limit_up_down():
    # 定义可买卖条件——未停牌、未涨跌停
    trade_status = dv.get_ts('trade_status')
    mask_sus = trade_status != 1
    # 涨停
    dv.add_formula('up_limit', '(close - Delay(close, 1)) / Delay(close, 1) > 0.095', is_quarterly=False, add_data=True)
    # 跌停
    dv.add_formula('down_limit', '(close - Delay(close, 1)) / Delay(close, 1) < -0.095', is_quarterly=False, add_data=True)
    can_enter = np.logical_and(dv.get_ts('up_limit') < 1, ~mask_sus) # 未涨停未停牌
    can_exit = np.logical_and(dv.get_ts('down_limit') < 1, ~mask_sus) # 未跌停未停牌
    return can_enter,can_exit

mask = mask_index_member()
can_enter,can_exit = limit_up_down()

print(mask.shape)
print(can_enter.shape)
print(dv.get_ts('close').shape)

from jaqs_fxdayu.research.signaldigger import multi_factor

ic = dict()
factors_dict = {signal:dv.get_ts(signal) for signal in FactorList}
Period=[18,19,20]
for period in Period:
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

import pandas as pd
ic_mean_table = pd.DataFrame(data=np.nan,columns=Period,index=FactorList)
ic_std_table = pd.DataFrame(data=np.nan,columns=Period,index=FactorList)
ir_table = pd.DataFrame(data=np.nan,columns=Period,index=FactorList)
for signal in FactorList:
    for period in Period:
        ic_mean_table.loc[signal,period]=ic[period][signal].mean()
        ic_std_table.loc[signal,period]=ic[period][signal].std()
        ir_table.loc[signal,period]=ic[period][signal].mean()/ic[period][signal].std()

print(ic_mean_table)
print(ic_std_table)
print(ir_table)


ic_mean_table.plot(kind="barh",xerr=ic_std_table,figsize=(15,5))
ir_table.plot(kind="barh",figsize=(15,5))

FactorList = ['MoneyFlow20','TVSTD20','TVMA6','TVSTD6']  #输入因子合成阶段要使用的因子

from jaqs_fxdayu.research.signaldigger import process
dv.add_field('sw1')
factor_dict = dict()
index_member = ~mask
for name in FactorList:
    print(name)
    signal = -1 * dv.get_ts(name)  # 调整符号

    signal = process.winsorize(factor_df=signal, alpha=0.05, index_member=index_member)  # 去极值

    # 行业中性化
    signal = process.neutralize(signal,
                                group=dv.get_ts("sw1"),  # 行业分类标准
                                )

    signal = process.standardize(signal, index_member)  # z-score标准化 保留排序信息和分布信息
    #     signal = process.rank_standardize(signal,index_member) #因子在截面排序并归一化到0-1(只保留排序信息)
    print('OK!')
    factor_dict[name] = signal

# 因子间存在较强同质性时，使用施密特正交化方法对因子做正交化处理，用得到的正交化残差作为因子
new_factors = multi_factor.orthogonalize(factors_dict=factor_dict,
                           standardize_type="z_score",#输入因子标准化方法，有"rank"（排序标准化）,"z_score"(z-score标准化)两种（"rank"/"z_score"）
                           winsorization=False,#是否对输入因子去极值
                           index_member=index_member) #　是否只处理指数成分股

# rollback_period代表滚动窗口所用到的天数,即用前多少期的数据来计算现阶段的因子权重。 通常建议设置时间在半年以上,可以获得相对稳定的预期结果

#  多因子组合-动态加权参数配置
props = {
    'price':dv.get_ts("close_adj"),
    'high':dv.get_ts("high_adj"), # 可为空
    'low':dv.get_ts("low_adj"),# 可为空
    'ret_type': 'return',#可选参数还有upside_ret/downside_ret 则组合因子将以优化潜在上行、下行空间为目标
    'benchmark_price': dv.data_benchmark,  # 为空计算的是绝对收益　不为空计算相对收益
    'period': 20, # 20天的持有期
    'mask': mask,
    'can_enter': can_enter,
    'can_exit': can_exit,
    'forward': True,
    'commission': 0.0008,
    "covariance_type": "shrink",  # 协方差矩阵估算方法 还可以为"simple"
    "rollback_period": 250}  # 滚动窗口天数

comb_factors = dict()
for method in ["equal_weight","ic_weight","ir_weight","max_IR","max_IC"]:
    comb_factors[method] = multi_factor.combine_factors(factor_dict,
                                                        standardize_type="z_score", #有"rank"（排序标准化）,"z_score"(z-score标准化)两种
                                                        winsorization=False,
                                                        weighted_method=method,
                                                        props=props)
    print(method)
    print(comb_factors[method].dropna(how="all").head())

period = 20
ic_20  =   multi_factor.get_factors_ic_df(comb_factors,
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
ic_20.head()

ic_20_mean = dict()
ic_20_std = dict()
ir_20 = dict()
for name in ic_20.columns:
    ic_20_mean[name]=ic_20[name].loc[20170101:].mean()
    ic_20_std[name]=ic_20[name].loc[20170101:].std()
    # ic_20_mean[name]=ic_20[name].loc[:].mean()
    # ic_20_std[name]=ic_20[name].loc[:].std()
    ir_20[name] = ic_20_mean[name]/ic_20_std[name]

import datetime

trade_date = pd.Series(ic_20.index)
trade_date = trade_date.apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
ic_20.index = trade_date

print(ic_20_mean["equal_weight"])
print(ic_20_mean["ic_weight"])
print(ir_20["equal_weight"])
print(ir_20["ic_weight"])

# 相对收益
import matplotlib.pyplot as plt
from jaqs_fxdayu.research.signaldigger.analysis import analysis
from jaqs_fxdayu.research import SignalDigger

obj = SignalDigger()
obj.process_signal_before_analysis(signal=comb_factors["ic_weight"],
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