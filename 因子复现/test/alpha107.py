#type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param = None):
    defult_param = {'t':1}
    if not param:
        param = defult_param

    t = param['t']

    alpha107 = dv.add_formula('alpha107',
                              '(((-1 * Rank((open - Delay(high, %s)))) * Rank((open - Delay(close, %s)))) * Rank((open - Delay(low, %s))))'%(t,t,t),
                              is_quarterly=False, add_data=True)
    return alpha107

