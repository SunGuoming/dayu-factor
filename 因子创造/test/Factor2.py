# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):
    defult_param = {'t': 60}
    if not param:
        param = defult_param

    t = param['t']

    EMA = dv.get_ts('close').ewm(span=t, adjust=False).mean()

    dv.append_df(EMA, 'EMA')
    Factor2 = dv.add_formula('Factor2',
                             'close-EMA',
                             is_quarterly=False, add_data=True)

    return Factor2

