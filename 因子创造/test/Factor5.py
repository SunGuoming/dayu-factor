# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t1': 3}
    if not param:
        param = defult_param

    t1 = param['t1']

    Factor5 = dv.add_formula('Factor5', '-VOL240-%s*VOL10'%(t1), is_quarterly=False, add_data=True)

    return Factor5

