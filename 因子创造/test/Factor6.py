# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 10}
params_description = {'t': '暂无'}
def run_formula(dv, param=None):
    """
    日均换手率与十日指数收益的合成
    """

    if not param:
        param = default_params

    t = param['t']

    dv.add_formula('dayr_10', 'close/Delay(close,%s)' % (t), is_quarterly=False, add_data=True)
    Factor6 = dv.add_formula('Factor6', '-VOL10*(dayr_10)-VOL10', is_quarterly=False, add_data=True)

    return Factor6

