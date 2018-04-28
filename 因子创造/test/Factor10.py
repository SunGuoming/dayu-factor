#type3  -  the intermediate variable of the factor is also a factor

def run_formula(dv):

    Factor10 = dv.add_formula('Factor10', 'BullPower*volume', is_quarterly=False, add_data=True)

    return Factor10

