# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 20}
params_description = {'t': '暂无'}
def run_formula(dv, param=None):
    """
    5日换手率与变形的Factor2的乘积
    """

    if not param:
        param = default_params

    t = param['t']

    Factor9 = dv.add_formula('Factor9', '-VOL5*(Ts_Sum(close_adj,%s)/%s-close_adj)'%(t,t), is_quarterly=False, add_data=True)

    return Factor9

