#type3  -  the intermediate variable of the factor is also a factor


def run_formula(dv, param = None):
    defult_param = {'t1':1,'t2':20}
    if not param:
        param = defult_param

    t1 = param['t1']
    t2 = param['t2']

    alpha110 = dv.add_formula("alpha110",
                              "Ts_Sum(Max(0,high-Delay(close,%s)),%s)/Ts_Sum(Max(0,Delay(close,%s)-low),%s)*100"%(t1,t2,t1,t2),
                              is_quarterly=False,add_data=True)
    return alpha110