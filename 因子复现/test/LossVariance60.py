# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t2': 60, 't1': 60} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t2': '暂无', 't1': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    60日损失方差
    """
    dv.add_formula('daily_return_no_reinv',
                   'close_adj/Delay(close_adj,1)-1',
                   is_quarterly=False, add_data=True)

    LossVariance60 = dv.add_formula('LossVariance60_J', "250*Ts_Sum(If(daily_return_no_reinv>0,0,daily_return_no_reinv*daily_return_no_reinv-daily_return_no_reinv),%s)/Ts_Sum(If(daily_return_no_reinv>0,0,1),%s)"%(params['t1'],params['t2']),
        is_quarterly=False, add_data=True)
    return LossVariance60
