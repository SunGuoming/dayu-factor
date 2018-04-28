#type2  -  only use add_formula function with parameter
        
def run_formula(dv, param = None):
    defult_param = {'t':60}
    if not param:
        param = defult_param

    t = param['t']

    BIAS60_J = dv.add_formula('BIAS60_J',
           '(close_adj/Ts_Sum(close_adj,%s)*%s-1)*100'%(t,t),
           is_quarterly=False)
    
    return BIAS60_J