# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t2': 60, 't1': 60} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t2': '暂无', 't1': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    60日乖离率，简称Y值，是移动平均原理派生的一项技术指标，表示股价偏离趋向指标斩百分比值。
    """
    BIAS60 = dv.add_formula('BIAS60_J', "(close_adj/Ts_Sum(close_adj,%s)*%s-1)*100"%(params['t1'],params['t2']),
        is_quarterly=False, add_data=True)
    return BIAS60
