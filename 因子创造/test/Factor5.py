## encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 3}
params_description = {'t': '暂无'}
def run_formula(dv, param=None):
    """
    过去240个交易日日均换手率加三倍的过去10个交易日日均换手率，加三倍过去10日日均换手率是提高敏感度，防止漏识别刚激动的股票
    """

    if not param:
        param = default_params

    t = param['t']

    Factor5 = dv.add_formula('Factor5', '-VOL240-%s*VOL10'%(t), is_quarterly=False, add_data=True)

    return Factor5

