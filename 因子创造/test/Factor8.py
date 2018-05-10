# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t1': 1, 't2': 20}
params_description = {'t1': '暂无', 't2': '暂无'}
def run_formula(dv, param=None):
    """
    过去20日指数涨幅的和
    """

    if not param:
        param = default_params

    t1 = param['t1']
    t2 = param['t2']

    dv.add_formula('a', 'close/Delay(close,%s)-1'%(t1), is_quarterly=False, add_data=True)
    Factor8 = dv.add_formula('Factor8', 'Ts_Sum(Max(a,0),%s)'%(t2), is_quarterly=False, add_data=True)

    return Factor8

