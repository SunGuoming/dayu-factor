#type3  -  the intermediate variable of the factor is also a factor


def run_formula(dv, param = None):
    defult_param = {'t1':1,'t2':13}
    if not param:
        param = defult_param
        
    t1 = param['t1']
    t2 = param['t2']

    DMZ = dv.add_formula('DMZ','If((high+low)>(Delay(high,%s)+Delay(low,%s)),Max(Abs(high-Delay(high,%s)),Abs(low-Delay(low,%s))),0)'%(t1,t1,t1,t1),
                         is_quarterly=False,
                         add_data=True)
    DMF = dv.add_formula('DMF','If((high+low)<(Delay(high,%s)+Delay(low,%s)),Max(Abs(high-Delay(high,%s)),Abs(low-Delay(low,%s))),0)'%(t1,t1,t1,t1),
                         is_quarterly=False,
                         add_data=True)


    DIZ_J = dv.add_formula("DIZ_J",
                           'Ts_Sum(DMZ,%s)/(Ts_Sum(DMZ,%s)+Ts_Sum(DMF,%s))'%(t2,t2,t2),
           is_quarterly=False,
           add_data=True)

    return DIZ_J