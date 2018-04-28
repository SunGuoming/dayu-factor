# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t': 60, 't1': 5}
    if not param:
        param = defult_param

    t = param['t']
    t1 = param['t1']

    Factor3 = dv.add_formula('Factor3',
                             'Ts_Sum(close,%s)/%s-Ts_Sum(close,%s)/%s'%(t,t,t1,t1),
                             is_quarterly=False, add_data=True)

    return Factor3

