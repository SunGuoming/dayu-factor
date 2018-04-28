# type2  -  only use add_formula function with parameter

def run_formula(dv, param=None):
    defult_param = {'t': 4}
    if not param:
        param = defult_param

    t = param['t']

    OperatingRevenueGrowRate_J = dv.add_formula('OperatingRevenueGrowRate_J',
                                              'TTM(oper_profit)/TTM(Delay(oper_profit,%s))-1'%(t), is_quarterly=True,
                                              add_data=True)

    return OperatingRevenueGrowRate_J
