# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t1': 1, 't2': 20}
    if not param:
        param = defult_param

    t1 = param['t1']
    t2 = param['t2']

    dv.add_formula('a', 'close/Delay(close,%s)-1'%(t1), is_quarterly=False, add_data=True)
    Factor8 = dv.add_formula('Factor8', 'Ts_Sum(Max(a,0),%s)'%(t2), is_quarterly=False, add_data=True)

    return Factor8

