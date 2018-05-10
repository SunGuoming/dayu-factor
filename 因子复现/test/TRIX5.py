# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    5日收盘价三重指数平滑移动平均指标（Triple Exponentially Smoothed Average）
    """
    EMA = dv.get_ts('close').ewm(span=5, adjust=False).mean()
    EMA2 = EMA.ewm(span=5, adjust=False).mean()
    EMA3 = EMA2.ewm(span=5, adjust=False).mean()
    dv.append_df(EMA3, 'EMA3')
    TRIX5 = dv.add_formula('TRIX5_J', "EMA3/Delay(EMA3,1)-1"%(),
        is_quarterly=False, add_data=True)
    return TRIX5
