# type3  -  the intermediate variable of the factor is also a factor


def run_formula(dv, param=None):
    defult_param = {'t1': 1, 't2': 60}
    if not param:
        param = defult_param

    t1 = param['t1']
    t2 = param['t2']

    dv.add_formula('daily_return_no_reinv',
                   'close_adj/Delay(close_adj,%s)-1'%(t1),
                   is_quarterly=False, add_data=True)

    LossVariance60 = dv.add_formula('LossVariance60',
                                    '250*Ts_Sum(If(daily_return_no_reinv>0,0,daily_return_no_reinv*daily_return_no_reinv-daily_return_no_reinv),%s)/Ts_Sum(If(daily_return_no_reinv>0,0,1),%s)'%(t2,t2),
                                    is_quarterly=False, add_data=True)

    return LossVariance60