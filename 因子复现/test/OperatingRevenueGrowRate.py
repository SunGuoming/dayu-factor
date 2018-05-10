# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t1': 4} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {'t1': '暂无'} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    营业收入增长率
    """
    OperatingRevenueGrowRate = dv.add_formula('OperatingRevenueGrowRate_J', "TTM(oper_profit)/TTM(Delay(oper_profit,%s))-1"%(params['t1']),
        is_quarterly=True, add_data=True)
    return OperatingRevenueGrowRate
