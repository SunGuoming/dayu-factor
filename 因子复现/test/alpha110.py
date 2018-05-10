# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t2': 20, 't4': 20, 't1': 1, 't3': 1} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t2': '暂无', 't4': '暂无', 't1': '暂无', 't3': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    alpha因子110
    """
    alpha110 = dv.add_formula('alpha110', "Ts_Sum(Max(0,high-Delay(close,%s)),%s)/Ts_Sum(Max(0,Delay(close,%s)-low),%s)*100"%(params['t1'],params['t2'],params['t3'],params['t4']),
        is_quarterly=False, add_data=True)
    return alpha110
