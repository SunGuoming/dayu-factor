# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
def run_formula(dv, param=None):
    """
    24月累计收益与空头力度的乘积
    """

    Factor7 = dv.add_formula('Factor7', 'CMRA*BullPower', is_quarterly=False, add_data=True)

    return Factor7

