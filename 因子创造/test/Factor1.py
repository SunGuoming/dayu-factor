# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t': 5, 't1': 20}
    if not param:
        param = defult_param

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

