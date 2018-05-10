# encoding: utf-8
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = 'SunGuoming' # 这里填下你的名字
default_params = {'t': 5, 't1': 20}
params_description = {'t': '暂无', 't1': '暂无'}
def run_formula(dv, param=None):
    """
    a为指数收益，b为20日均指数收益。该式意义为a>b时与a<b时ab二范数的比值。可以体现市场波动。
    """

    if not param:
        param = default_params

    t = param['t']
    t1 = param['t1']

    EMA = dv.get_ts('close').ewm(span=t, adjust=False).mean()
    EMA2 = EMA.ewm(span=t, adjust=False).mean()
    EMA3 = EMA2.ewm(span=t, adjust=False).mean()
    dv.append_df(EMA3, 'EMA3')
    dv.add_formula('a', 'close/Delay(close,1)-1', is_quarterly=False, add_data=True)
    dv.add_formula('b', '(close/Delay(EMA3,%s))^(1/%s)-1' % (t1 - 1, t1), is_quarterly=False, add_data=True)
    Factor1 = dv.add_formula('Factor1',
                             '-Log((Ts_Sum(If(a>b,1,0),%s)-1)*Ts_Sum(If(a<b,(a-b)^2,0),%s)/(Ts_Sum(If(a<b,1,0),%s))*Ts_Sum(If(a>b,(a-b)^2,0),%s))' % (t1, t1, t1, t1),
                             is_quarterly=False, add_data=True)

    return Factor1

