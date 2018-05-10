# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 60, 't1': 5}
params_description = {'t': '暂无', 't1': '暂无'}
def run_formula(dv, param=None):
    """
    反金叉
    """

    if not param:
        param = default_params

    t = param['t']
    t1 = param['t1']

    Factor3 = dv.add_formula('Factor3',
                             'Ts_Sum(close,%s)/%s-Ts_Sum(close,%s)/%s'%(t,t,t1,t1),
                             is_quarterly=False, add_data=True)

    return Factor3

