# -*- coding: utf-8 -*-
from Model.globalInfo import GlobalInfo
from Control.DBManager import connMySQL

class StatTableData:

    def __init__(self):
        self.dbobj =  connMySQL()

    def GetOverviewData(self):
        model =[]
        for row, underlying in enumerate(GlobalInfo.p_underlyingType):
            idcondition = 'punderlying = "'  + str( underlying) + '"'
            _lst =  self.dbobj.selectValue('tradingbook',  ['count(*)','sum(actualnotamt)','sum(actualpremium)' ,'sum(notamt)'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            # if _lst[0][0] ==0:
            #     con_cnt = con_cnt+1
            #     continue
            # row = row -con_cnt
            temp = [0]*10
            temp[0] = underlying
            temp[1] = _lst[0][0] 

            if _lst[0][1] ==None:
                temp[4] = 0
            else:
                temp[4] = _lst[0][1] 

            if _lst[0][2] ==None:
                temp[5] = 0
            else:
                temp[5] = _lst[0][2] 
            
            if _lst[0][3] ==None:
                temp[7] = 0
            else:
                temp[7] = _lst[0][3] 

            _lst =  self.dbobj.selectValue('tradingbook',  [ 'count(*)'], 'punderlying = "'  + str( underlying) + '" and contractstatus != 1')
            temp[2] = _lst[0][0] 
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'count(*)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            temp[3] = _lst[0][0] 
            
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(actualnotamt)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            # print '-----',_lst,_lst[0][0]
            if _lst[0][0] ==None:
                temp[6] = 0
            else:
                temp[6] = _lst[0][0] 
            
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '"')
            if _lst[0][0] ==None:
                temp[8] = 0
            else:
                temp[8] = _lst[0][0] 
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            if _lst[0][0] ==None:
                temp[9] = 0
            else:
                temp[9] = _lst[0][0]
            model.append(temp)
        temp = [0]*10

        temp[0] = 'Total'

        for i in range(1,10):
            temp[i] = self.GetColSum(model,i)
        model.append(temp)

        return model


    def GetSS(self):
        model =[]
        for row, underlying in enumerate(GlobalInfo.p_underlyingType):
            temp = [underlying]
            
            idcondition = 'recorddate in (select max(recorddate) from newprofitandloss) and '+ 'underlying = "'  + str( underlying) + '"' 
            _lst =  self.dbobj.selectValue('newprofitandloss',  ['underlyingpnl','dayunderlyingpnl', 'closepriceunderlyingpnl','closepricedayunderlyingpnl'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            if _lst == []:
                temp.append(0)
                temp.append(0)
                temp.append(0)
                temp.append(0)
            else:
                temp.append(_lst[0][0])
                temp.append(_lst[0][1])
                temp.append(_lst[0][2])
                temp.append(_lst[0][3])
            idcondition = 'recorddate in (select max(recorddate) from greeksunderlying) and underlying = "'  + str( underlying) + '"'
            _lst =  self.dbobj.selectValue('greeksunderlying',  ['closeprice'], idcondition)  #获取最新期货损益  
            udlprice =0
            if _lst==[]:
                udlprice =0
            else:
                udlprice = _lst[0][0]

            idcondition = 'punderlying = "'  + str( underlying) + '" and contractstatus = 1 '
            _lst = self.dbobj.selectValue('tradingbook',  ['sum(delta)'], idcondition)
            if _lst[0][0] ==None:
                _value = 0
            else:
                _value = self.get_hold_data(underlying) - udlprice *_lst[0][0]
            temp.append(_value)

            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '"')
            _value = 0
            if _lst[0][0] ==None:
                _value = 0
            else:
                _value = _lst[0][0] 
            temp.append(_value)
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            if _lst[0][0] ==None:
                _value = 0
            else:
                _value = _lst[0][0] 
            temp.append(_value)

            model.append(temp)
        temp = [0]*8

        temp[0] = u'合计'

        for i in range(1,8):
            temp[i] = self.GetColSum(model,i)
        model.append(temp)

        return model

    def get_hold_data(self, underlying):
        
        _lst = self.holdnum(underlying)
            
        lstlen = len(_lst)
        sum_closeprice_hedgeamt = 0

        for i in range(0, lstlen):
            # print _lst
            closeprice_hedgeamt = int(_lst[i][3])*_lst[i][7]*_lst[i][6]
            sum_closeprice_hedgeamt = sum_closeprice_hedgeamt + closeprice_hedgeamt

        
        return sum_closeprice_hedgeamt

    def holdnum(self, underlying):
        # print 'cal hold amount'
        _numArr = []
        idcondition = 'underlying = "'  + str( underlying) + '"'
        _lstinfo =  self.dbobj.selectValue('transaction',  ['distinct(code)'], idcondition)  

        for elm in _lstinfo:
            _numList = []
            idcondition = 'code = "'  + str( elm[0]) + '"'
            _numList.append(elm[0])

            _num =  self.dbobj.selectValue('transaction',  ['sum(dealnum)'], 'code = "'  + str( elm[0]) + '" and askbid = 1')
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            _num =  self.dbobj.selectValue('transaction',  ['-sum(dealnum)'], 'code = "'  + str( elm[0]) + '" and askbid = 2')
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            _num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition)  
            
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            idcondition = 'entrustdate < (select max(entrustdate) from transaction) and code = "'  + str(  elm[0]) + '"'
            pre_num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition) 
            if pre_num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(pre_num[0][0])

            # _numList.append(pre_num[0][0]) 

            # print _num[0][0],elm[0]
            if _num[0][0] == 0:
                continue  #pass
            else:
                # print _num[0][0],elm[0]
                idcondition = 'recorddate in (select max(recorddate) from settle) and code = "'  + str(  elm[0]) + '"'
                _price =  self.dbobj.selectValue('settle',  ['settleprice', 'coefficient', 'closeprice'], idcondition)  #获取最新期货损益 
                if _price == []:
                    _numList.append(0)
                    _numList.append(0)
                    _numList.append(0)
                else:
                    _numList.append( _price[0][0])
                    _numList.append( _price[0][1])
                    _numList.append( _price[0][2])

                _numArr.append(_numList)
        
        return _numArr

    def summarypnl(self):
        model =[]
        today = str( GlobalInfo.today)
        for row, underlying in enumerate(GlobalInfo.p_underlyingType):
            idcondition = 'punderlying = "'  + str( underlying) + '"'
            _lst =  self.dbobj.selectValue('tradingbook',  ['count(*)','sum(actualnotamt)','sum(actualpremium)' ,'sum(notamt)'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            # if _lst[0][0] ==0:
            #     con_cnt = con_cnt+1
            #     continue
            # row = row -con_cnt
            temp = [0]*11
            temp[0] = today
            temp[1] = underlying
            temp[2] = _lst[0][0] 

            if _lst[0][1] ==None:
                temp[5] = 0
            else:
                temp[5] = _lst[0][1] 

            if _lst[0][2] ==None:
                temp[6] = 0
            else:
                temp[6] = _lst[0][2] 
            
            if _lst[0][3] ==None:
                temp[8] = 0
            else:
                temp[8] = _lst[0][3] 

            _lst =  self.dbobj.selectValue('tradingbook',  [ 'count(*)'], 'punderlying = "'  + str( underlying) + '" and contractstatus != 1')
            temp[3] = _lst[0][0] 
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'count(*)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            temp[4] = _lst[0][0] 
            
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(actualnotamt)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            # print '-----',_lst,_lst[0][0]
            if _lst[0][0] ==None:
                temp[7] = 0
            else:
                temp[7] = _lst[0][0] 
            
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '"')
            if _lst[0][0] ==None:
                temp[9] = 0
            else:
                temp[9] = _lst[0][0] 
            _lst =  self.dbobj.selectValue('tradingbook',  [ 'sum(maxpayment)'], 'punderlying = "'  + str( underlying) + '" and contractstatus = 1')
            if _lst[0][0] ==None:
                temp[10] = 0
            else:
                temp[10] = _lst[0][0]

            idcondition = 'recorddate in (select max(recorddate) from newprofitandloss) and '+ 'underlying = "'  + str( underlying) + '"' 
            _lst =  self.dbobj.selectValue('newprofitandloss',  ['closepriceunderlyingpnl', 'closepriceunderlyingtde','underlyingdnl' ,'underlyingpremium','underlyingpayout','underlyingprice', 'underlyingtde','underlyingpnl'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            if _lst == []:
                temp.extend([0]*8)
            else:
                temp.extend(_lst[0])
            if temp not in model:
                model.append(temp)

        return model

    def GetColSum(self,arr, col):
        _sum = 0
        for elm in arr:
            _sum = _sum + elm[col]

        return _sum

    def GetResultsData(self):
        model =[]
        for row, underlying in enumerate(GlobalInfo.p_underlyingType):
            idcondition = 'recorddate in (select max(recorddate) from newprofitandloss) and '+ 'underlying = "'  + str( underlying) + '"' 
            _lst =  self.dbobj.selectValue('newprofitandloss',  ['underlyingpnl','underlyingtde','underlyingdnl' ,'underlyingpremium','underlyingpayout','underlyingprice',\
                                                                'dayunderlyingpnl','dayunderlyingtde','dayunderlyingdnl' ,'dayunderlyingpremium','dayunderlyingpayout','dayunderlyingprice'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            temp = [0]
            temp[0] = underlying
            temp.extend(_lst[0])
            model.append(temp)
        temp = [0]*13
        temp[0] = 'Total'

        for i in range(1,13):
            temp[i] = self.GetColSum(model,i)
        model.append(temp)

        return model

    def GetPositionData(self):
        pass

    def GetRiskMonitorData(self):
        pass

    def GetTransactionFlowData(self):
        pass


if __name__ == '__main__':
    self.std = StatTableData()
    print self.std.GetResultsData()