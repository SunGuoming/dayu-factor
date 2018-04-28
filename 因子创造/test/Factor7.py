# type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv, param=None):

    Factor7 = dv.add_formula('Factor7', 'CMRA*BullPower', is_quarterly=False, add_data=True)

    return Factor7

