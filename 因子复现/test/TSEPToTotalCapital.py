#type3  -  the intermediate variable of the factor is also a factor


def run_formula(dv):


    TSEPToTotalCapital = dv.add_formula('TSEPToTotalCapital', 'tot_shrhldr_eqy_incl_min_int/tot_assets',
                                        is_quarterly=False, add_data=True)

    return TSEPToTotalCapital

