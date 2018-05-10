# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t2': 1, 't1': 1, 't3': 1} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t2': '暂无', 't1': '暂无', 't3': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    alpha因子107
    """
    alpha107 = dv.add_formula('alpha107', "(((-1 * Rank((open - Delay(high, %s)))) * Rank((open - Delay(close, %s)))) * Rank((open - Delay(low, %s))))"%(params['t1'],params['t2'],params['t3']),
        is_quarterly=False, add_data=True)
    return alpha107
