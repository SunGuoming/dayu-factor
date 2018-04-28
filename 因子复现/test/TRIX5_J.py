#type2  -  only use add_formula function with parameter
        
def run_formula(dv, param = None):
    defult_param = {'t1':3,'t2':6,'t3':12,'t4':24}
    if not param:
        param = defult_param
    
    BBI = dv.add_formula('BBI_J', 
           '''Ta('MA',0,open,high,low,close,volume,%s)+Ta('MA',0,open,high,low,close,volume,%s)+Ta('MA',0,open,high,low,close,volume,%s)+
           Ta('MA',0,open,high,low,close,volume,%s)/4'''%(param['t1'],param['t2'],param['t3'],param['t4']),
           is_quarterly=False)
    OperatingRevenueGrowRate = dv.add_formula('OperatingRevenueGrowRate_J',
                                              'TTM(oper_profit)/TTM(Delay(oper_profit,4))-1', is_quarterly=True,
                                              add_data=True)
    return BBI
