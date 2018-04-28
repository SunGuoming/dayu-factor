#type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param = None):
    defult_param = {'t1':10,'t2':30}
    if not param:
        param = defult_param

    t1 = param['t1']
    t2 = param['t2']

    dv.add_formula('dayr_10', 'close/Delay(close,%s)'%(t1), is_quarterly=False, add_data=True)
    Factor4 = dv.add_formula('Factor4', '-Ts_Sum(dayr_10,%s)'%(t2), is_quarterly=False, add_data=True)

    return Factor4

