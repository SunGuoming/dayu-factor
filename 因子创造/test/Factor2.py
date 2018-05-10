# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 60}
params_description = {'t': '暂无'}
def run_formula(dv, param=None):
    """
    收盘价与60日指数均线值的差，类似60日乖离率
    """

    if not param:
        param = default_params

    t = param['t']

    EMA = dv.get_ts('close').ewm(span=t, adjust=False).mean()

    dv.append_df(EMA, 'EMA')
    Factor2 = dv.add_formula('Factor2',
                             'close-EMA',
                             is_quarterly=False, add_data=True)

    return Factor2

