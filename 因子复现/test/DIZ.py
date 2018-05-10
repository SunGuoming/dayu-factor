# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t2': 13, 't1': 13, 't3': 13} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t2': '暂无', 't1': '暂无', 't3': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    未预期盈余（Standardized unexpected earnings）
    """
    DIZ = dv.add_formula('DIZ_J', "Ts_Sum(If((high+low)>(Delay(high,1)+Delay(low,1)),Max(Abs(high-Delay(high,1)),Abs(low-Delay(low,1))),0),%s)/(Ts_Sum(If((high+low)>(Delay(high,1)+Delay(low,1)),Max(Abs(high-Delay(high,1)),Abs(low-Delay(low,1))),0),%s)+Ts_Sum(If((high+low)<(Delay(high,1)+Delay(low,1)),Max(Abs(high-Delay(high,1)),Abs(low-Delay(low,1))),0),%s))"%(params['t1'],params['t2'],params['t3']),
        is_quarterly=False, add_data=True)
    return DIZ
