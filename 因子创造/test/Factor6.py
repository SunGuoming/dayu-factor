# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t1': 10}
    if not param:
        param = defult_param

    t1 = param['t1']

    dv.add_formula('dayr_10', 'close/Delay(close,%s)' % (t1), is_quarterly=False, add_data=True)
    Factor6 = dv.add_formula('Factor6', '-VOL10*(dayr_10)-VOL10', is_quarterly=False, add_data=True)

    return Factor6

