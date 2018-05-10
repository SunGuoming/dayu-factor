# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
def run_formula(dv):
    """
    空头力度与成交量的乘积
    """

    Factor10 = dv.add_formula('Factor10', 'BullPower*volume', is_quarterly=False, add_data=True)

    return Factor10

