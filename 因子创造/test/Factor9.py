# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t1': 20}
    if not param:
        param = defult_param

    t1 = param['t1']

    Factor9 = dv.add_formula('Factor9', '-VOL5*(Ts_Sum(close_adj,%s)/%s-close_adj)'%(t1,t1), is_quarterly=False, add_data=True)

    return Factor9

